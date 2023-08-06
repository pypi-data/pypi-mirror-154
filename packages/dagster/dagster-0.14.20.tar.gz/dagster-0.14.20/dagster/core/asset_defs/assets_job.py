import itertools
from typing import (
    AbstractSet,
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import dagster._check as check
from dagster.config import Shape
from dagster.core.definitions.asset_layer import AssetLayer
from dagster.core.definitions.config import ConfigMapping
from dagster.core.definitions.dependency import (
    DependencyDefinition,
    IDependencyDefinition,
    NodeHandle,
    NodeInvocation,
)
from dagster.core.definitions.events import AssetKey
from dagster.core.definitions.executor_definition import ExecutorDefinition
from dagster.core.definitions.graph_definition import GraphDefinition
from dagster.core.definitions.job_definition import JobDefinition
from dagster.core.definitions.node_definition import NodeDefinition
from dagster.core.definitions.output import OutputDefinition
from dagster.core.definitions.partition import PartitionedConfig, PartitionsDefinition
from dagster.core.definitions.partition_key_range import PartitionKeyRange
from dagster.core.definitions.resource_definition import ResourceDefinition
from dagster.core.errors import DagsterInvalidDefinitionError
from dagster.core.selector.subset_selector import AssetSelectionData
from dagster.utils.backcompat import experimental

from .asset_partitions import get_upstream_partitions_for_partition_range
from .assets import AssetsDefinition
from .source_asset import SourceAsset


@experimental
def build_assets_job(
    name: str,
    assets: Iterable[AssetsDefinition],
    source_assets: Optional[Sequence[Union[SourceAsset, AssetsDefinition]]] = None,
    resource_defs: Optional[Mapping[str, ResourceDefinition]] = None,
    description: Optional[str] = None,
    config: Optional[Union[ConfigMapping, Dict[str, Any], PartitionedConfig]] = None,
    tags: Optional[Dict[str, Any]] = None,
    executor_def: Optional[ExecutorDefinition] = None,
    _asset_selection_data: Optional[AssetSelectionData] = None,
) -> JobDefinition:
    """Builds a job that materializes the given assets.

    The dependencies between the ops in the job are determined by the asset dependencies defined
    in the metadata on the provided asset nodes.

    Args:
        name (str): The name of the job.
        assets (List[AssetsDefinition]): A list of assets or
            multi-assets - usually constructed using the :py:func:`@asset` or :py:func:`@multi_asset`
            decorator.
        source_assets (Optional[Sequence[Union[SourceAsset, AssetsDefinition]]]): A list of
            assets that are not materialized by this job, but that assets in this job depend on.
        resource_defs (Optional[Dict[str, ResourceDefinition]]): Resource defs to be included in
            this job.
        description (Optional[str]): A description of the job.

    Examples:

        .. code-block:: python

            @asset
            def asset1():
                return 5

            @asset
            def asset2(asset1):
                return my_upstream_asset + 1

            my_assets_job = build_assets_job("my_assets_job", assets=[asset1, asset2])

    Returns:
        JobDefinition: A job that materializes the given assets.
    """

    check.str_param(name, "name")
    check.iterable_param(assets, "assets", of_type=AssetsDefinition)
    check.opt_sequence_param(
        source_assets, "source_assets", of_type=(SourceAsset, AssetsDefinition)
    )
    check.opt_str_param(description, "description")
    check.opt_inst_param(_asset_selection_data, "_asset_selection_data", AssetSelectionData)
    source_assets_by_key = build_source_assets_by_key(source_assets)

    deps, assets_defs_by_node_handle = build_deps(assets, source_assets_by_key.keys())
    partitioned_config = build_job_partitions_from_assets(assets, source_assets or [])
    resource_defs = check.opt_mapping_param(resource_defs, "resource_defs")

    graph = GraphDefinition(
        name=name,
        node_defs=[asset.node_def for asset in assets],
        dependencies=deps,
        description=description,
        input_mappings=None,
        output_mappings=None,
        config=None,
    )

    all_resource_defs = dict(resource_defs)
    for asset_def in assets:
        for resource_key, resource_def in asset_def.resource_defs.items():
            if (
                resource_key in all_resource_defs
                and all_resource_defs[resource_key] != resource_def
            ):
                raise DagsterInvalidDefinitionError(
                    f"When attempting to build job, asset {asset_def.asset_key} had a conflicting version of the same resource key {resource_key}. Please resolve this conflict by giving different keys to each resource definition."
                )
            all_resource_defs[resource_key] = resource_def

    # turn any AssetsDefinitions into SourceAssets
    resolved_source_assets: List[SourceAsset] = []
    for asset in source_assets or []:
        if isinstance(asset, AssetsDefinition):
            resolved_source_assets += asset.to_source_assets()
        elif isinstance(asset, SourceAsset):
            resolved_source_assets.append(asset)

    return graph.to_job(
        resource_defs=all_resource_defs,
        config=config or partitioned_config,
        tags=tags,
        executor_def=executor_def,
        asset_layer=AssetLayer.from_graph_and_assets_node_mapping(
            graph, assets_defs_by_node_handle, resolved_source_assets
        ),
        _asset_selection_data=_asset_selection_data,
    )


def build_job_partitions_from_assets(
    assets: Iterable[AssetsDefinition],
    source_assets: Sequence[Union[SourceAsset, AssetsDefinition]],
) -> Optional[PartitionedConfig]:
    assets_with_partitions_defs = [assets_def for assets_def in assets if assets_def.partitions_def]

    if len(assets_with_partitions_defs) == 0:
        return None

    first_assets_with_partitions_def: AssetsDefinition = assets_with_partitions_defs[0]
    for assets_def in assets_with_partitions_defs:
        if assets_def.partitions_def != first_assets_with_partitions_def.partitions_def:
            first_asset_key = next(iter(assets_def.asset_keys)).to_string()
            second_asset_key = next(iter(first_assets_with_partitions_def.asset_keys)).to_string()
            raise DagsterInvalidDefinitionError(
                "When an assets job contains multiple partitions assets, they must have the "
                f"same partitions definitions, but asset '{first_asset_key}' and asset "
                f"'{second_asset_key}' have different partitions definitions. "
            )

    partitions_defs_by_asset_key: Dict[AssetKey, PartitionsDefinition] = {}
    asset: Union[AssetsDefinition, SourceAsset]
    for asset in itertools.chain.from_iterable([assets, source_assets]):
        if isinstance(asset, AssetsDefinition) and asset.partitions_def is not None:
            for asset_key in asset.asset_keys:
                partitions_defs_by_asset_key[asset_key] = asset.partitions_def
        elif isinstance(asset, SourceAsset) and asset.partitions_def is not None:
            partitions_defs_by_asset_key[asset.key] = asset.partitions_def

    def asset_partitions_for_job_partition(
        job_partition_key: str,
    ) -> Mapping[AssetKey, PartitionKeyRange]:
        return {
            asset_key: PartitionKeyRange(job_partition_key, job_partition_key)
            for assets_def in assets
            for asset_key in assets_def.asset_keys
            if assets_def.partitions_def
        }

    def run_config_for_partition_fn(partition_key: str) -> Dict[str, Any]:
        ops_config: Dict[str, Any] = {}
        asset_partitions_by_asset_key = asset_partitions_for_job_partition(partition_key)

        for assets_def in assets:
            outputs_dict: Dict[str, Dict[str, Any]] = {}
            if assets_def.partitions_def is not None:
                for output_name, asset_key in assets_def.asset_keys_by_output_name.items():
                    asset_partition_key_range = asset_partitions_by_asset_key[asset_key]
                    outputs_dict[output_name] = {
                        "start": asset_partition_key_range.start,
                        "end": asset_partition_key_range.end,
                    }

            inputs_dict: Dict[str, Dict[str, Any]] = {}
            for input_name, in_asset_key in assets_def.asset_keys_by_input_name.items():
                upstream_partitions_def = partitions_defs_by_asset_key.get(in_asset_key)
                if assets_def.partitions_def is not None and upstream_partitions_def is not None:
                    upstream_partition_key_range = get_upstream_partitions_for_partition_range(
                        assets_def, upstream_partitions_def, in_asset_key, asset_partition_key_range
                    )
                    inputs_dict[input_name] = {
                        "start": upstream_partition_key_range.start,
                        "end": upstream_partition_key_range.end,
                    }

            config_schema = assets_def.node_def.config_schema
            if (
                config_schema
                and isinstance(config_schema.config_type, Shape)
                and "assets" in config_schema.config_type.fields
            ):
                ops_config[assets_def.node_def.name] = {
                    "config": {
                        "assets": {
                            "input_partitions": inputs_dict,
                            "output_partitions": outputs_dict,
                        }
                    }
                }

        return {"ops": ops_config}

    return PartitionedConfig(
        partitions_def=cast(PartitionsDefinition, first_assets_with_partitions_def.partitions_def),
        run_config_for_partition_fn=lambda p: run_config_for_partition_fn(p.name),
    )


def build_source_assets_by_key(
    source_assets: Optional[Sequence[Union[SourceAsset, AssetsDefinition]]]
) -> Mapping[AssetKey, Union[SourceAsset, OutputDefinition]]:
    source_assets_by_key: Dict[AssetKey, Union[SourceAsset, OutputDefinition]] = {}
    for asset_source in source_assets or []:
        if isinstance(asset_source, SourceAsset):
            source_assets_by_key[asset_source.key] = asset_source
        elif isinstance(asset_source, AssetsDefinition):
            for output_name, asset_key in asset_source.asset_keys_by_output_name.items():
                if asset_key:
                    source_assets_by_key[asset_key] = asset_source.node_def.output_def_named(
                        output_name
                    )

    return source_assets_by_key


def build_deps(
    assets_defs: Iterable[AssetsDefinition], source_paths: AbstractSet[AssetKey]
) -> Tuple[
    Dict[Union[str, NodeInvocation], Dict[str, IDependencyDefinition]],
    Mapping[NodeHandle, AssetsDefinition],
]:
    node_outputs_by_asset: Dict[AssetKey, Tuple[NodeDefinition, str]] = {}
    assets_defs_by_node_handle: Dict[NodeHandle, AssetsDefinition] = {}

    for assets_def in assets_defs:
        for output_name, asset_key in assets_def.asset_keys_by_output_name.items():
            if asset_key in node_outputs_by_asset:
                raise DagsterInvalidDefinitionError(
                    f"The same asset key was included for two definitions: '{asset_key.to_string()}'"
                )

            node_outputs_by_asset[asset_key] = (assets_def.node_def, output_name)

    deps: Dict[Union[str, NodeInvocation], Dict[str, IDependencyDefinition]] = {}
    # if the same graph/op is used in multiple assets_definitions, their invocations much have
    # different names. we keep track of definitions that share a name and add a suffix to their
    # invocations to solve this issue
    collisions: Dict[str, int] = {}
    for assets_def in assets_defs:
        node_name = assets_def.node_def.name
        if collisions.get(node_name):
            collisions[node_name] += 1
            alias = f"{node_name}_{collisions[node_name]}"
            node_key = NodeInvocation(node_name, alias)
        else:
            collisions[node_name] = 1
            alias = node_name
            node_key = node_name
        deps[node_key] = {}
        assets_defs_by_node_handle[NodeHandle(alias, parent=None)] = assets_def
        for input_name, asset_key in sorted(
            assets_def.asset_keys_by_input_name.items(), key=lambda input: input[0]
        ):  # sort so that input definition order is deterministic
            if asset_key in node_outputs_by_asset:
                node_def, output_name = node_outputs_by_asset[asset_key]
                deps[node_key][input_name] = DependencyDefinition(node_def.name, output_name)
            elif asset_key not in source_paths:
                input_def = assets_def.node_def.input_def_named(input_name)
                if not input_def.dagster_type.is_nothing:
                    raise DagsterInvalidDefinitionError(
                        f"Input asset '{asset_key.to_string()}' for asset "
                        f"'{next(iter(assets_def.asset_keys)).to_string()}' is not "
                        "produced by any of the provided asset ops and is not one of the provided "
                        "sources"
                    )

    return deps, assets_defs_by_node_handle
