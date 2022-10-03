import pytest

from pepy.application.badge_service import DownloadsNumberFormatter
from pepy.domain.model import Downloads, BadgeUnits


@pytest.fixture
def downloads_formatter():
    return DownloadsNumberFormatter()


def test_downloads_format_0(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(0)
    assert "0" == downloads_formatter.format(downloads)


def test_downloads_format_less_than_thousands(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(121)
    assert "121" == downloads_formatter.format(downloads)


def test_downloads_format_thousands(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(12132)
    assert "12k" == downloads_formatter.format(downloads)


def test_downloads_format_million(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(412_132_492)
    assert "412M" == downloads_formatter.format(downloads)


def test_downloads_format_billion(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(9_132_919_492)
    assert "9G" == downloads_formatter.format(downloads)


def test_downloads_format_trillion(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(11_132_919_492_000)
    assert "11T" == downloads_formatter.format(downloads)


def test_downloads_format_quadrillion(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(11_132_919_492_432_000)
    assert "11P" == downloads_formatter.format(downloads)


def test_downloads_format_with_abbreviation_0(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(0)
    assert "0" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)


def test_downloads_format_with_abbreviation_less_than_thousands(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(121)
    assert "121" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)


def test_downloads_format_with_abbreviation_thousands(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(12132)
    assert "12k" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)


def test_downloads_format_with_abbreviation_million(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(412_132_492)
    assert "412M" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)


def test_downloads_format_with_abbreviation_billion(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(9_132_919_492)
    assert "9B" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)


def test_downloads_format_with_abbreviation_trillion(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(11_132_919_492_000)
    assert "11T" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)


def test_downloads_format_with_abbreviation_quadrillion(downloads_formatter: DownloadsNumberFormatter):
    downloads = Downloads(11_132_919_492_432_000)
    assert "11Q" == downloads_formatter.format_with_units(downloads, BadgeUnits.abbreviation)
