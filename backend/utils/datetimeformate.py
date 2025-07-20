from datetime import datetime, timezone

def parse_iso_datetime(dt_str: str) -> datetime:
    """Parses an ISO 8601 string and returns a timezone-aware UTC datetime."""
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
