import datetime
from typing import Iterable

from google.cloud.bigquery import Client
from google.cloud.bigquery.table import RowIterator

from pepy.domain.pypi import StatsViewer, Result, Row


class BQStatsViewer(StatsViewer):
    TIMEOUT = 20 * 60  # timeout of 20 minutes
    PAGE_SIZE = 5_000

    def __init__(self, client: Client):
        self.client = client

    def get_version_downloads(self, date: datetime.date) -> Result:
        QUERY = """
            SELECT file.project as project, file.version as version, count(*) AS downloads, countif(details.installer.name = 'pip') as pip_downloads
            FROM `the-psf.pypi.file_downloads`
            WHERE timestamp >= '{}' AND timestamp < '{}'
            GROUP BY file.project, file.version
            ORDER BY file.project
        """.format(
            date.strftime("%Y-%m-%d"), date + datetime.timedelta(days=1)
        )

        query_job = self.client.query(QUERY, location="US")
        query_job.result(self.TIMEOUT)
        destination = query_job.destination
        destination = self.client.get_table(destination)
        rows = self.client.list_rows(destination, page_size=self.PAGE_SIZE)
        return Result(rows.total_rows, self._transform_rows(rows, date))

    @staticmethod
    def _transform_rows(row_iterator: RowIterator, date: datetime.date) -> Iterable[Row]:
        for row in row_iterator:
            yield Row(row.get("project"), row.get("version"), date, row.get("downloads"), row.get("pip_downloads"))
