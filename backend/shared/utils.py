import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def prettify_service_name(service_slug: str) -> str:
    if not service_slug:
        return service_slug
    if service_slug.startswith("amazon-"):
        rest = service_slug[len("amazon-"):]
        return "Amazon " + rest.replace("-", " ").title()
    elif service_slug.startswith("aws-"):
        rest = service_slug[len("aws-"):]
        return "AWS " + rest.replace("-", " ").title()
    else:
        return service_slug.replace("-", " ").title()


def parse_rfc2822_to_iso(date_str: str) -> str:
    try:
        dt = parsedate_to_datetime(date_str)
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def strip_html(html: str) -> str:
    if not html:
        return ""
    clean = re.sub(r'<[^>]+>', '', html)
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&gt;', '>')
    clean = clean.replace('&quot;', '"')
    clean = clean.replace('&#39;', "'")
    clean = clean.replace('&nbsp;', ' ')
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean
