from datetime import datetime, timezone

def utc() -> datetime:
    return datetime.now(timezone.utc)

def format(datetime: datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
