import json
import os
import sys
import logging
from datetime import datetime, timezone
from urllib import request
import xml.etree.ElementTree as ET

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, '/var/task/shared')
from utils import parse_rfc2822_to_iso, strip_html

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['TABLE_NAME']
QUEUE_URL = os.environ['QUEUE_URL']
SSM_PARAM_PREFIX = os.environ.get('SSM_PARAM_PREFIX', '/app/features')
RSS_URL = 'https://aws.amazon.com/new/feed/'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')
ssm = boto3.client('ssm', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)


def fetch_rss() -> bytes:
    req = request.Request(RSS_URL, headers={'User-Agent': 'aws-features-tracker/1.0'})
    with request.urlopen(req, timeout=30) as resp:
        return resp.read()


def parse_rss(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    channel = root.find('channel')
    items = []
    for item_el in channel.findall('item'):
        title = (item_el.findtext('title') or '').strip()
        link = (item_el.findtext('link') or '').strip()
        pub_date_raw = (item_el.findtext('pubDate') or '').strip()
        description_raw = (item_el.findtext('description') or '').strip()
        guid = (item_el.findtext('guid') or link).strip()

        categories = [el.text.strip() for el in item_el.findall('category') if el.text]

        service_slug = ''
        item_type = ''
        for cat in categories:
            if 'products/' in cat and not service_slug:
                parts = cat.split('products/')
                if len(parts) > 1:
                    service_slug = parts[1].strip().lower()
            if 'marchitecture/' in cat and not item_type:
                parts = cat.split('marchitecture/')
                if len(parts) > 1:
                    item_type = parts[1].strip().lower()

        pub_date = parse_rfc2822_to_iso(pub_date_raw) if pub_date_raw else ''
        raw_description = strip_html(description_raw)

        items.append({
            'guid': guid,
            'title': title,
            'link': link,
            'pub_date': pub_date,
            'raw_description': raw_description,
            'service_slug': service_slug,
            'type': item_type,
        })
    return items


def guid_exists(guid: str) -> bool:
    try:
        resp = table.get_item(Key={'guid': guid}, ProjectionExpression='guid')
        return 'Item' in resp
    except ClientError as e:
        logger.error(f"DynamoDB GetItem error: {e}")
        return False


def write_pending(item: dict):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    table.put_item(Item={
        'guid': item['guid'],
        'title': item['title'],
        'link': item['link'],
        'pub_date': item['pub_date'],
        'raw_description': item['raw_description'],
        'service_slug': item['service_slug'],
        'type': item['type'],
        'status': 'pending',
        'created_at': now,
    })


def send_to_sqs(item: dict):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(item),
    )


def update_last_fetched():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ssm.put_parameter(
        Name=f'{SSM_PARAM_PREFIX}/last-fetched',
        Value=now,
        Type='String',
        Overwrite=True,
    )


def lambda_handler(event, context):
    logger.info("Fetcher starting")
    xml_bytes = fetch_rss()
    items = parse_rss(xml_bytes)
    logger.info(f"Parsed {len(items)} items from RSS feed")

    new_count = 0
    for item in items:
        if not item['guid']:
            continue
        if guid_exists(item['guid']):
            continue
        write_pending(item)
        send_to_sqs(item)
        new_count += 1

    update_last_fetched()
    logger.info(f"Found {new_count} new items, sent to SQS")
    return {'new_items': new_count}
