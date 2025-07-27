
import pytz
from datetime import datetime, timedelta,timezone

def parse_iso_datetime(dt_str: str) -> datetime:
    """Parses an ISO 8601 string and returns a timezone-aware UTC datetime."""
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

INDIA_TZ = pytz.timezone("Asia/Kolkata")
UTC = pytz.utc

def get_tomorrow_ist_bounds_as_utc():
    tomorrow_ist = datetime.now(INDIA_TZ).date() + timedelta(days=1)
    start_ist = INDIA_TZ.localize(datetime.combine(tomorrow_ist, datetime.min.time()))
    end_ist = INDIA_TZ.localize(datetime.combine(tomorrow_ist, datetime.max.time()))
    return start_ist.astimezone(UTC), end_ist.astimezone(UTC)

from datetime import datetime, timedelta

from datetime import datetime, timedelta

def get_previous_month_bounds_as_naive_utc():
    now_utc = datetime.utcnow()
    first_day_this_month = now_utc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_prev_month = first_day_this_month - timedelta(seconds=1)
    first_day_prev_month = last_day_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = (first_day_this_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_this_month = first_day_next_month - timedelta(seconds=1)
    return  first_day_this_month,last_day_this_month


