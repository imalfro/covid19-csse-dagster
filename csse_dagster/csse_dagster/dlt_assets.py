from dagster import AssetExecutionContext, AssetKey
from dlt.extract.resource import DltResource
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets, DagsterDltTranslator
from dlt import pipeline
from .dlt_sources.ccse import extract_daily_reports, extract_timeseries_reports
   
@dlt_assets(
    dlt_source=extract_daily_reports(
        sourcekey='daily_reports',
        git_folder='csse_covid_19_daily_reports'
    ),
    dlt_pipeline=pipeline(
        pipeline_name="daily_reports",
        dataset_name="ccse_covid19",
        destination="postgres",
        progress="log",
    ),
    name="daily_reports",
)
def dagster_daily_reports(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

@dlt_assets(
    dlt_source=extract_daily_reports(
        sourcekey='lookup_reference',
        filenames=['UID_ISO_FIPS_LookUp_Table.csv']
    ),
    dlt_pipeline=pipeline(
        pipeline_name="lookup_table",
        dataset_name="ccse_covid19",
        destination="postgres",
        progress="log",
    ),
    name="lookup_reference",
)
def dagster_lookup_reference(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

@dlt_assets(
    dlt_source=extract_timeseries_reports(
        sourcekey='global',
        id_vars=['Province/State','Country/Region','Lat','Long'],
        git_folder='csse_covid_19_time_series'
    ),
    dlt_pipeline=pipeline(
        pipeline_name="timeseries_global",
        dataset_name="ccse_covid19",
        destination="postgres",
        progress="log",
    ),
    name="timeseries_global",
)
def dagster_timeseries_global(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

@dlt_assets(
    dlt_source=extract_timeseries_reports(
        sourcekey='US',
        id_vars=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_','Combined_Key','Population'],
        git_folder='csse_covid_19_time_series'
    ),
    dlt_pipeline=pipeline(
        pipeline_name="timeseries_us",
        dataset_name="ccse_covid19",
        destination="postgres",
        progress="log",
    ),
    name="timeseries_us",
)
def dagster_timeseries_us(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)