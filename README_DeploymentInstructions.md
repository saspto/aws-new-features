# AWS Features Tracker — Deployment Instructions

## Prerequisites
- AWS CLI configured (`aws configure`) with a profile that has sufficient IAM permissions
- AWS SAM CLI installed (`sam --version`)
- Node.js 18+ and npm installed
- Python 3.12+ installed
- AWS_REGION=us-east-1

## Quick Deploy

```bash
cd /workshop/aws-new-features
chmod +x infrastructure/deploy.sh
AWS_REGION=us-east-1 ENVIRONMENT=dev bash infrastructure/deploy.sh
```

The script will:
1. Build all Lambda functions with `sam build`
2. Deploy the CloudFormation stack
3. Build the React frontend with Vite
4. Sync the built assets to the S3 frontend bucket
5. Print the CloudFront URL

## Load Mock Data

After deploy, load demo data so the app shows real content:

```bash
python3 infrastructure/load_mock_data.py --table aws-features --region us-east-1
```

This inserts 12 realistic AWS feature announcements with summaries, key points, and feature type classifications.

## Architecture

```
EventBridge (6hr) → Fetcher Lambda → SQS → Summarizer Lambda (Bedrock Claude Haiku)
                                              ↓
                                         DynamoDB + S3
CloudFront → S3 (React SPA)
CloudFront /api/* → API Gateway → API Lambda → DynamoDB
```

## Accessing the App

After deployment, the CloudFront URL is printed at the end of the deploy script.
Open it in a browser — the React SPA will load and show all summarized features.

The app supports:
- Full-text search (debounced)
- Filter by AWS service, feature type, date range
- Sort newest/oldest first
- Infinite scroll pagination
- Feature detail pages with full summaries and key points
- Direct links to AWS announcement pages

## Manual Trigger (Fetch Now)

To trigger an immediate RSS fetch instead of waiting 6 hours:

```bash
aws lambda invoke \
  --function-name aws-features-fetcher-dev \
  --payload '{}' \
  --region us-east-1 \
  /tmp/fetcher-output.json && cat /tmp/fetcher-output.json
```

## Stack Outputs

| Output | Description |
|--------|-------------|
| CloudFrontURL | Main application URL |
| ApiGatewayURL | Direct API Gateway URL |
| FrontendBucketName | S3 bucket for React SPA |
| SummariesBucketName | S3 bucket for JSON summaries |
| DynamoDBTableName | DynamoDB table name |

## Cost Estimate (~$0.31/month at low traffic)

| Service | Cost |
|---------|------|
| Lambda | ~$0.01 |
| DynamoDB on-demand | ~$0.02 |
| S3 | ~$0.03 |
| CloudFront | ~$0.10 |
| Bedrock Claude Haiku | ~$0.15 |
| SQS + EventBridge | $0.00 |

## Teardown

```bash
STACK_NAME=aws-features-tracker-dev
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Empty S3 buckets first
aws s3 rm s3://aws-features-frontend-${ACCOUNT_ID} --recursive
aws s3 rm s3://aws-features-summaries-${ACCOUNT_ID} --recursive

# Delete stack
aws cloudformation delete-stack --stack-name ${STACK_NAME} --region us-east-1
```
