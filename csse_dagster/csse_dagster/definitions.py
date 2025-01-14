from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource
from dagster_embedded_elt.dlt import DagsterDltResource

#from . import dlt_assets, dbt_assets
from .dlt_assets import dagster_lookup_reference, dagster_timeseries_global, dagster_timeseries_us
from .dbt_assets import dagster_dbt_dbt_assets
from .project import dagster_dbt_project
from .schedules import schedules

dlt_resource = DagsterDltResource()
#all_dlt_assets = load_assets_from_modules([dlt_assets])
#all_dbt_assets = load_assets_from_modules([dbt_assets])

defs = Definitions(
    assets=[dagster_lookup_reference, dagster_timeseries_global, dagster_timeseries_us, dagster_dbt_dbt_assets],#all_dlt_assets+all_dbt_assets,
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dagster_dbt_project),
        "dlt": dlt_resource,
    },
)