"""
calendar_ics.py — Read Outlook calendar from a published ICS link.
No Azure, no OAuth, no tokens. Just a URL.
"""

import urllib.request
from icalendar import Calendar
from datetime import datetime, date, timedelta, timezone
from typing import List, Dict, Tuple
import ssl


def fetch_ics_events(ics_url: str, target_date: date = None) -> List[Dict]:
    """
    Fetch events from an ICS URL for the target date.
    Returns list of {subject, start, end, duration_minutes}.
    """
    target_date = target_date or date.today()
    
    # Fetch ICS data
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(ics_url, headers={"User-Agent": "RecipeBot/1.0"})
    resp = urllib.request.urlopen(req, context=ctx, timeout=10)
    cal = Calendar.from_ical(resp.read())
    
    events = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        
        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        if not dtstart or not dtend:
            continue
        
        start = dtstart.dt
        end = dtend.dt
        
        # Handle all-day events (date, not datetime)
        if isinstance(start, date) and not isinstance(start, datetime):
            continue  # Skip all-day events
        
        # Normalize to naive local datetime for comparison
        if hasattr(start, "tzinfo") and start.tzinfo:
            start = start.astimezone(tz=None).replace(tzinfo=None)
        if hasattr(end, "tzinfo") and end.tzinfo:
            end = end.astimezone(tz=None).replace(tzinfo=None)
        
        # Filter to target date
        if start.date() != target_date and end.date() != target_date:
            continue
        
        summary = str(component.get("summary", "(No title)"))
        duration = int((end - start).total_seconds() / 60)
        
        events.append({
            "subject": summary,
            "start": start,
            "end": end,
            "duration_minutes": duration,
        })
    
    events.sort(key=lambda e: e["start"])
    return events


def calculate_free_time(
    events: List[Dict],
    target_date: date = None,
    window_start_hour: int = 17,
    window_end_hour: int = 21,
) -> Tuple[int, str, List[Dict]]:
    """
    Calculate free cooking time in the evening window.
    Returns (free_minutes, summary_text, event_list).
    """
    target_date = target_date or date.today()
    window_start = datetime(target_date.year, target_date.month, target_date.day, window_start_hour)
    window_end = datetime(target_date.year, target_date.month, target_date.day, window_end_hour)
    
    # Filter events that overlap with the cooking window
    evening_events = []
    for e in events:
        if e["end"] <= window_start or e["start"] >= window_end:
            continue
        evening_events.append(e)
    
    if not evening_events:
        total = int((window_end - window_start).total_seconds() / 60)
        return total, f"Evening is clear — full {total} minutes free ({window_start_hour}–{window_end_hour} PM)", evening_events
    
    # Merge overlapping busy intervals
    intervals = sorted([
        (max(e["start"], window_start), min(e["end"], window_end))
        for e in evening_events
    ])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    # Compute free blocks
    busy_minutes = sum(int((e - s).total_seconds() / 60) for s, e in merged)
    total_window = int((window_end - window_start).total_seconds() / 60)
    free = total_window - busy_minutes
    
    event_names = ", ".join(f"{e['subject']} ({e['start'].strftime('%I:%M %p')})" for e in evening_events)
    summary = f"{free} min free tonight · {len(evening_events)} event(s): {event_names}"
    
    return free, summary, evening_events


def get_cooking_window(ics_url: str = None, target_date: date = None) -> Tuple[int, str]:
    """High-level: fetch calendar, calculate free time."""
    if not ics_url:
        return 90, "No calendar connected — assuming 90 min free."
    
    try:
        events = fetch_ics_events(ics_url, target_date)
        free, summary, _ = calculate_free_time(events, target_date)
        return free, summary
    except Exception as e:
        return 90, f"Couldn't read calendar ({e}) — assuming 90 min free."
