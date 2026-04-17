import json
import os
import sys
import base64
import logging
import time
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

sys.path.insert(0, '/var/task/shared')
from utils import prettify_service_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

_services_cache = {'data': None, 'ts': 0}
_types_cache = {'data': None, 'ts': 0}
CACHE_TTL = 300


def json_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def respond(status_code: int, body: dict, headers: dict = None) -> dict:
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    if headers:
        default_headers.update(headers)
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body, default=json_default),
    }


def scan_all_summarized() -> list[dict]:
    filter_expr = Attr('status').eq('summarized')
    items = []
    kwargs = {
        'FilterExpression': filter_expr,
    }
    while True:
        resp = table.scan(**kwargs)
        items.extend(resp.get('Items', []))
        last_key = resp.get('LastEvaluatedKey')
        if not last_key:
            break
        kwargs['ExclusiveStartKey'] = last_key
    return items


def format_item(item: dict) -> dict:
    key_points = item.get('key_points', [])
    if isinstance(key_points, set):
        key_points = list(key_points)

    return {
        'guid': item.get('guid', ''),
        'title': item.get('title', ''),
        'service_slug': item.get('service_slug', ''),
        'service_name': prettify_service_name(item.get('service_slug', '')),
        'type': item.get('type', ''),
        'feature_type': item.get('feature_type', ''),
        'pub_date': item.get('pub_date', ''),
        'link': item.get('link', ''),
        'summary': item.get('summary', ''),
        'key_points': key_points,
        'summarized_at': item.get('summarized_at', ''),
    }


def handle_features(params: dict) -> dict:
    q = (params.get('q') or '').lower().strip()
    service = (params.get('service') or '').lower().strip()
    ftype = (params.get('type') or '').lower().strip()
    from_date = params.get('from_date', '').strip()
    to_date = params.get('to_date', '').strip()
    sort = params.get('sort', 'date_desc')
    try:
        limit = min(max(int(params.get('limit', 20)), 1), 100)
    except (ValueError, TypeError):
        limit = 20
    next_token_enc = params.get('next_token', '')

    items = scan_all_summarized()

    if q:
        filtered = []
        for item in items:
            searchable = ' '.join([
                item.get('title', ''),
                item.get('summary', ''),
                item.get('service_slug', ''),
            ]).lower()
            if q in searchable:
                filtered.append(item)
        items = filtered

    if service:
        items = [i for i in items if i.get('service_slug', '').lower() == service]

    if ftype:
        items = [i for i in items if i.get('feature_type', '').lower() == ftype]

    if from_date:
        items = [i for i in items if i.get('pub_date', '') >= from_date]

    if to_date:
        items = [i for i in items if i.get('pub_date', '') <= to_date + 'T23:59:59Z']

    reverse = sort != 'date_asc'
    items.sort(key=lambda x: x.get('pub_date', ''), reverse=reverse)

    total_count = len(items)

    start = 0
    if next_token_enc:
        try:
            token_data = json.loads(base64.b64decode(next_token_enc).decode())
            start = token_data.get('offset', 0)
        except Exception:
            start = 0

    page = items[start:start + limit]
    new_next_token = None
    if start + limit < total_count:
        new_next_token = base64.b64encode(json.dumps({'offset': start + limit}).encode()).decode()

    return {
        'items': [format_item(i) for i in page],
        'next_token': new_next_token,
        'total_count': total_count,
    }


def handle_feature_detail(guid: str) -> dict:
    resp = table.get_item(Key={'guid': guid})
    item = resp.get('Item')
    if not item:
        return None
    return format_item(item)


def handle_services() -> list[dict]:
    now = time.time()
    if _services_cache['data'] and now - _services_cache['ts'] < CACHE_TTL:
        return _services_cache['data']

    items = scan_all_summarized()
    counts = {}
    for item in items:
        slug = item.get('service_slug', '')
        if slug:
            counts[slug] = counts.get(slug, 0) + 1

    result = [{'service_slug': k, 'count': v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    _services_cache['data'] = result
    _services_cache['ts'] = now
    return result


def handle_types() -> list[dict]:
    now = time.time()
    if _types_cache['data'] and now - _types_cache['ts'] < CACHE_TTL:
        return _types_cache['data']

    items = scan_all_summarized()
    counts = {}
    for item in items:
        ft = item.get('feature_type', '')
        if ft:
            counts[ft] = counts.get(ft, 0) + 1

    result = [{'feature_type': k, 'count': v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    _types_cache['data'] = result
    _types_cache['ts'] = now
    return result


def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    path = event.get('rawPath', '/')
    params = event.get('queryStringParameters') or {}

    if method == 'OPTIONS':
        return respond(200, {})

    if path == '/health':
        return respond(200, {
            'status': 'ok',
            'timestamp': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    if path == '/features' or path == '/api/features':
        result = handle_features(params)
        return respond(200, result)

    if path.startswith('/features/') or path.startswith('/api/features/'):
        guid = path.split('/features/')[-1].strip('/')
        item = handle_feature_detail(guid)
        if item is None:
            return respond(404, {'error': 'Feature not found'})
        return respond(200, item)

    if path == '/services' or path == '/api/services':
        return respond(200, handle_services())

    if path == '/types' or path == '/api/types':
        return respond(200, handle_types())

    return respond(404, {'error': 'Not found'})
