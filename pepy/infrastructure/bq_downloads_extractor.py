import datetime
from typing import List

from google.cloud.bigquery import Client

from pepy.domain.model import ProjectDownloads, ProjectName, Downloads
from pepy.domain.repository import DownloadsExtractor


class BQDownloadsExtractor(DownloadsExtractor):
    TIMEOUT = 5 * 60 # timeout of 5 minutes

    def __init__(self, client: Client):
        self.client = client

    def get_downloads(self, date: datetime.date) -> List[ProjectDownloads]:
        QUERY = """
            SELECT file.project as name, count(*) AS downloads
            FROM `the-psf.pypi.downloads{}`
            GROUP BY file.project
        """.format(date.strftime("%Y%m%d"))

        query_job = self.client.query(QUERY, location='US')
        query_result = query_job.result(self.TIMEOUT)
        result = []
        for row in query_result:
            name = ProjectName(row['name'])
            downloads = Downloads(row['downloads'])
            result.append(ProjectDownloads(name, downloads))

        return result
