import json
import os
import sys
import logging
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, '/var/task/shared')
from utils import prettify_service_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['TABLE_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-haiku-4-5-20251001-v1:0')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

SYSTEM_PROMPT = "You are a technical writer summarizing AWS announcements for engineers. Be concise and factual."

USER_PROMPT_TEMPLATE = """Summarize this AWS announcement in 3-5 sentences. Focus on: what the feature does, who it benefits, and any key technical details or limits. Return a JSON object with these fields only:
{{
  "summary": "3-5 sentence summary",
  "feature_type": "one of: new-feature | enhancement | preview | general-availability | deprecation | price-change | region-expansion | integration",
  "key_points": ["bullet 1", "bullet 2", "bullet 3"]
}}

Title: {title}
Description: {description}"""


def invoke_bedrock(title: str, description: str) -> dict:
    truncated_desc = description[:2000]
    user_content = USER_PROMPT_TEMPLATE.format(title=title, description=truncated_desc)

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_content}],
    })

    resp = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType='application/json',
        accept='application/json',
        body=body,
    )
    resp_body = json.loads(resp['body'].read())
    text = resp_body['content'][0]['text']

    json_match = text.strip()
    start = json_match.find('{')
    end = json_match.rfind('}')
    if start != -1 and end != -1:
        json_match = json_match[start:end+1]

    return json.loads(json_match)


def update_dynamo(guid: str, summary_data: dict):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    table.update_item(
        Key={'guid': guid},
        UpdateExpression='SET #s = :s, feature_type = :ft, key_points = :kp, #st = :status, summarized_at = :sa',
        ExpressionAttributeNames={'#s': 'summary', '#st': 'status'},
        ExpressionAttributeValues={
            ':s': summary_data['summary'],
            ':ft': summary_data['feature_type'],
            ':kp': summary_data['key_points'],
            ':status': 'summarized',
            ':sa': now,
        },
    )


def update_dynamo_error(guid: str, error_msg: str):
    table.update_item(
        Key={'guid': guid},
        UpdateExpression='SET #st = :status, error_message = :err',
        ExpressionAttributeNames={'#st': 'status'},
        ExpressionAttributeValues={
            ':status': 'error',
            ':err': error_msg[:1000],
        },
    )


def write_to_s3(guid: str, item: dict, summary_data: dict):
    now = datetime.now(timezone.utc)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    key = f"summaries/{year}/{month}/{guid}.json"

    enriched = {
        **item,
        'summary': summary_data['summary'],
        'feature_type': summary_data['feature_type'],
        'key_points': summary_data['key_points'],
        'service_name': prettify_service_name(item.get('service_slug', '')),
        'summarized_at': now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        'status': 'summarized',
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(enriched, ensure_ascii=False),
        ContentType='application/json',
    )


def process_record(record: dict):
    body = json.loads(record['body'])
    guid = body['guid']
    title = body.get('title', '')
    raw_description = body.get('raw_description', '')

    logger.info(f"Processing guid={guid}, title={title[:80]}")

    summary_data = invoke_bedrock(title, raw_description)

    required_keys = {'summary', 'feature_type', 'key_points'}
    if not required_keys.issubset(summary_data.keys()):
        raise ValueError(f"Bedrock response missing keys: {required_keys - summary_data.keys()}")

    if not isinstance(summary_data['key_points'], list):
        summary_data['key_points'] = [str(summary_data['key_points'])]

    update_dynamo(guid, summary_data)
    write_to_s3(guid, body, summary_data)
    logger.info(f"Successfully processed guid={guid}")


def lambda_handler(event, context):
    records = event.get('Records', [])
    logger.info(f"Processing {len(records)} SQS messages")

    batch_item_failures = []

    for record in records:
        message_id = record['messageId']
        guid = ''
        try:
            body = json.loads(record['body'])
            guid = body.get('guid', message_id)
            process_record(record)
        except Exception as e:
            logger.error(f"Error processing message {message_id} guid={guid}: {e}", exc_info=True)
            try:
                if guid:
                    update_dynamo_error(guid, str(e))
            except Exception as dynamo_err:
                logger.error(f"Failed to update error status for guid={guid}: {dynamo_err}")
            batch_item_failures.append({'itemIdentifier': message_id})

    return {'batchItemFailures': batch_item_failures}
