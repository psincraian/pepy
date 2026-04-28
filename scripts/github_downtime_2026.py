"""Scrape GitHub status incidents for 2026 and print a daily calendar.

Each day in 2026 (up to today) is rendered as:
    🟩  no incident reported on githubstatus.com
    ⬜  one or more services were degraded or down

Usage:
    python scripts/github_downtime_2026.py
"""
from __future__ import annotations

import calendar
import datetime as dt
import re
import sys
from html.parser import HTMLParser
from urllib.request import Request, urlopen

YEAR = 2026
STATUS_API = "https://www.githubstatus.com/api/v2/incidents.json"
HISTORY_URL = "https://www.githubstatus.com/history?page={page}"
USER_AGENT = "pepy-github-downtime-scraper/1.0"

GREEN = "\U0001F7E9"
WHITE = "⬜️"

MONTH_NAMES = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}


def _http_get(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_api_incidents() -> list[dict]:
    import json

    data = json.loads(_http_get(STATUS_API))
    return data.get("incidents", [])


class _HistoryParser(HTMLParser):
    """Extract incident dates from a Statuspage HTML history page."""

    _MONTH_RE = re.compile(r"([A-Za-z]+)\s+(\d{4})")
    _DAY_RE = re.compile(r"(\d{1,2})")

    def __init__(self) -> None:
        super().__init__()
        self.dates: set[dt.date] = set()
        self._current_month: tuple[int, int] | None = None
        self._capture: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k: v or "" for k, v in attrs}
        cls = attr_map.get("class", "")
        if tag in {"h2", "h3"} and "month" in cls.lower():
            self._capture = "month"
            self._buf = []
        elif "date" in cls.lower() and "incident" in cls.lower():
            self._capture = "day"
            self._buf = []
        elif tag == "var" and attr_map.get("data-var") == "date":
            self._capture = "day"
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if not self._capture:
            return
        text = "".join(self._buf).strip()
        if self._capture == "month":
            m = self._MONTH_RE.search(text)
            if m:
                month = MONTH_NAMES.get(m.group(1).lower())
                year = int(m.group(2))
                if month:
                    self._current_month = (year, month)
        elif self._capture == "day" and self._current_month:
            d = self._DAY_RE.search(text)
            if d:
                year, month = self._current_month
                try:
                    self.dates.add(dt.date(year, month, int(d.group(1))))
                except ValueError:
                    pass
        self._capture = None
        self._buf = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf.append(data)


def fetch_history_dates(max_pages: int = 6) -> set[dt.date]:
    """Walk monthly history pages until we've covered all of YEAR."""
    found: set[dt.date] = set()
    for page in range(1, max_pages + 1):
        html = _http_get(HISTORY_URL.format(page=page))
        parser = _HistoryParser()
        parser.feed(html)
        if not parser.dates:
            break
        found.update(parser.dates)
        if min(parser.dates).year < YEAR:
            break
    return found


def incident_dates_from_api(incidents: list[dict]) -> set[dt.date]:
    dates: set[dt.date] = set()
    for inc in incidents:
        start_raw = inc.get("started_at") or inc.get("created_at")
        if not start_raw:
            continue
        start = dt.datetime.fromisoformat(start_raw.replace("Z", "+00:00")).date()
        end_raw = inc.get("resolved_at") or inc.get("updated_at")
        end = (
            dt.datetime.fromisoformat(end_raw.replace("Z", "+00:00")).date()
            if end_raw
            else start
        )
        day = start
        while day <= end:
            dates.add(day)
            day += dt.timedelta(days=1)
    return dates


def collect_incident_dates() -> set[dt.date]:
    api_dates = incident_dates_from_api(fetch_api_incidents())
    history_dates = fetch_history_dates()
    return {d for d in api_dates | history_dates if d.year == YEAR}


def render_calendar(incident_dates: set[dt.date], today: dt.date) -> str:
    lines: list[str] = []
    for month in range(1, 13):
        first = dt.date(YEAR, month, 1)
        if first > today:
            break
        last_day = calendar.monthrange(YEAR, month)[1]
        end = min(dt.date(YEAR, month, last_day), today)
        cells = []
        for day in range(1, end.day + 1):
            d = dt.date(YEAR, month, day)
            cells.append(WHITE if d in incident_dates else GREEN)
        lines.append(f"{first.strftime('%B'):<10} {''.join(cells)}")
    return "\n".join(lines)


def main() -> int:
    today = dt.date.today()
    if today.year < YEAR:
        print(f"Year {YEAR} has not started yet.", file=sys.stderr)
        return 1
    incidents = collect_incident_dates()
    print(f"GitHub status — {YEAR} (through {today.isoformat()})")
    print(f"{GREEN} = no incidents   {WHITE} = one or more services degraded\n")
    print(render_calendar(incidents, min(today, dt.date(YEAR, 12, 31))))
    print(f"\nTotal days with incidents in {YEAR}: {len(incidents)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
