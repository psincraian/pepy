import pytest

from pepy.application.query import DownloadsNumberFormatter
from pepy.domain.model import Downloads


@pytest.fixture
def downloads_formatter():
    return DownloadsNumberFormatter()


def test_downloads_format_less_than_thousands(downloads_formatter: DownloadsNumberFormatter):
    downloads = 121
    assert "121" == downloads_formatter.format(downloads)


def test_downloads_format_thousands(downloads_formatter: DownloadsNumberFormatter):
    downloads = 12132
    assert "12k" == downloads_formatter.format(downloads)


def test_downloads_format_million(downloads_formatter: DownloadsNumberFormatter):
    downloads = 412_132_492
    assert "412M" == downloads_formatter.format(downloads)


def test_downloads_format_billion(downloads_formatter: DownloadsNumberFormatter):
    downloads = 9_132_919_492
    assert "9B" == downloads_formatter.format(downloads)


def test_downloads_format_trillion(downloads_formatter: DownloadsNumberFormatter):
    downloads = 11_132_919_492_000
    assert "11T" == downloads_formatter.format(downloads)


def test_downloads_format_quadrillion(downloads_formatter: DownloadsNumberFormatter):
    downloads = 11_132_919_492_432_000
    assert "11Q" == downloads_formatter.format(downloads)
