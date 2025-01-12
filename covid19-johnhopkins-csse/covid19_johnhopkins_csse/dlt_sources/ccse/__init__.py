from typing import Sequence

import dlt
from dlt.sources import DltResource

from .helpers import get_csvs


@dlt.source
def daily_reports(
) -> Sequence[DltResource]:
    """
    csse_covid_19_daily_reports
    """
    return (
        dlt.resource(
            get_csvs(
                "csse_covid_19_daily_reports",
            ),
            name="daily_reports",
            write_disposition="replace",
        ),
    )