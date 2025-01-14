from typing import Sequence

import dlt
from dlt.sources import DltResource

from .helpers import get_csvs, get_timeseries_csvs


@dlt.source
def extract_daily_reports(
    sourcekey,
    git_folder='',
    filenames=None,
    write_disposition='replace'
) -> Sequence[DltResource]:
    """
    csse_covid_19_daily_reports
    """
    return (
        dlt.resource(
            get_csvs(
                key=sourcekey,
                dir=git_folder,
                filenames=filenames,
            ),
            name=sourcekey,
            write_disposition=write_disposition,
        ),
    )

@dlt.source
def extract_timeseries_reports(
    sourcekey,
    id_vars,
    git_folder='',
    filenames=None,
    write_disposition='replace'
)-> Sequence[DltResource]:
    """
    csse_covid_19_time_series
    """
    return (
        dlt.resource(
            get_timeseries_csvs(
                key=sourcekey,
                dir=git_folder,
                filenames=filenames,
                id_vars=id_vars,
            ),
            name=f"timeseries_{sourcekey}",
            write_disposition=write_disposition,
        ),
    )