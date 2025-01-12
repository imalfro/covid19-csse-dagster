from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline
from dlt_sources.ccse import daily_reports


@dlt_assets(
    dlt_source=daily_reports(),
    dlt_pipeline=pipeline(
        pipeline_name="daily_reports",
        dataset_name="daily_reports",
        destination="postgres",
        progress="log",
    ),
    name="github",
    group_name="github",
)
def dagster_github_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)