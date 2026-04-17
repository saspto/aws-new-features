#!/usr/bin/env python3
"""
Load mock AWS feature announcements into DynamoDB for demo purposes.
Usage: python3 infrastructure/load_mock_data.py [--table aws-features] [--region us-east-1]
"""
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta

import boto3

MOCK_FEATURES = [
    {
        "guid": "mock-001-bedrock-kb-reranking",
        "title": "Amazon Bedrock Knowledge Bases now supports semantic reranking for improved RAG accuracy",
        "service_slug": "amazon-bedrock",
        "type": "ai-ml",
        "feature_type": "new-feature",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-bedrock-knowledge-bases-semantic-reranking/",
        "raw_description": "Amazon Bedrock Knowledge Bases now supports semantic reranking, allowing you to improve retrieval accuracy for Retrieval Augmented Generation (RAG) applications.",
        "summary": "Amazon Bedrock Knowledge Bases introduces semantic reranking to improve retrieval accuracy in RAG workflows. This feature uses a cross-encoder model to rerank retrieved documents based on relevance to the query, significantly reducing hallucinations. Engineers building RAG applications can enable reranking with a single API parameter. Supports both Amazon and Cohere reranking models. Available in all Bedrock-supported regions.",
        "key_points": [
            "Semantic reranking reduces RAG hallucinations by rescoring retrieved chunks",
            "Supports Amazon Rerank 1.0 and Cohere Rerank 3.5 models",
            "Enabled via RetrievalConfiguration.VectorSearchConfiguration.RerankingConfiguration"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-002-ec2-c8g-instances",
        "title": "Amazon EC2 C8g instances powered by AWS Graviton4 now generally available",
        "service_slug": "amazon-ec2",
        "type": "compute",
        "feature_type": "general-availability",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-ec2-c8g-instances-graviton4/",
        "raw_description": "Amazon EC2 C8g instances, powered by AWS Graviton4 processors, are now generally available. These instances deliver up to 40% better price performance compared to C7g instances for compute-intensive workloads.",
        "summary": "Amazon EC2 C8g instances powered by AWS Graviton4 are now GA. These instances deliver up to 40% better price performance vs C7g for compute-intensive workloads like HPC, batch processing, and web servers. Available in sizes from c8g.medium to c8g.48xlarge. Graviton4 provides 30% higher compute performance and 75% more L3 cache than Graviton3. Supported in us-east-1, us-west-2, and eu-west-1.",
        "key_points": [
            "Up to 40% better price performance vs C7g instances",
            "Graviton4 offers 30% higher compute performance and 75% more L3 cache than Graviton3",
            "Available from c8g.medium up to c8g.48xlarge with up to 192 vCPUs"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-003-rds-aurora-limitless",
        "title": "Amazon Aurora Limitless Database adds support for MySQL 8.0 compatible edition",
        "service_slug": "amazon-aurora",
        "type": "databases",
        "feature_type": "enhancement",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/aurora-limitless-mysql-8/",
        "raw_description": "Amazon Aurora Limitless Database now supports MySQL 8.0 compatible edition, enabling horizontal scaling for MySQL workloads without application changes.",
        "summary": "Aurora Limitless Database extends its horizontal scaling capabilities to MySQL 8.0 workloads. Previously only available for PostgreSQL, this enhancement lets teams scale MySQL databases beyond 100,000 writes/second and 100 TB without sharding application logic. The feature uses distributed SQL routing transparently. Existing Aurora MySQL 8.0 clusters can migrate with minimal downtime. Available in us-east-1 and us-west-2.",
        "key_points": [
            "Extends Limitless horizontal scaling to MySQL 8.0 compatible workloads",
            "Supports >100K writes/sec and >100 TB storage without application sharding",
            "Zero-ETL compatible with Amazon Redshift for analytics"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-004-lambda-response-streaming",
        "title": "AWS Lambda response streaming now supports binary content types",
        "service_slug": "aws-lambda",
        "type": "serverless",
        "feature_type": "enhancement",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=4)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/lambda-response-streaming-binary/",
        "raw_description": "AWS Lambda response streaming now supports binary content types including images, PDFs, and audio files, in addition to the previously supported text and JSON formats.",
        "summary": "AWS Lambda response streaming now handles binary content types like images, PDFs, and audio files alongside existing text/JSON support. This enables Lambda functions behind Function URLs or API Gateway to stream large binary responses directly without buffering. The max response size limit for streaming remains at 20 MB. Useful for media processing pipelines, document generation, and ML inference returning embeddings. No code changes needed beyond setting the response content-type header.",
        "key_points": [
            "Binary streaming adds support for image/*, application/pdf, audio/*, and application/octet-stream",
            "20 MB max streaming response size unchanged",
            "Works with Lambda Function URLs and API Gateway HTTP API"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-005-s3-express-replication",
        "title": "Amazon S3 Express One Zone now supports cross-account replication",
        "service_slug": "amazon-s3",
        "type": "storage",
        "feature_type": "new-feature",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/s3-express-one-zone-cross-account-replication/",
        "raw_description": "Amazon S3 Express One Zone now supports cross-account replication, allowing high-performance storage directories to be replicated across AWS accounts for data sharing and DR scenarios.",
        "summary": "S3 Express One Zone adds cross-account replication for its single-digit millisecond latency directory buckets. Teams can now replicate high-throughput workloads across AWS accounts for disaster recovery, data lake sharing, or multi-account architectures. Replication is configured via S3 Replication Rules with IAM cross-account trust policies. Replication lag is typically under 15 minutes. Replicated data maintains Express One Zone performance characteristics in the destination account.",
        "key_points": [
            "Replication configured via standard S3 Replication Rules API with cross-account IAM trust",
            "Typical replication lag under 15 minutes for Express One Zone",
            "Destination directory buckets must be pre-created in same or different availability zones"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-006-eks-auto-mode",
        "title": "Amazon EKS Auto Mode now available in 10 additional AWS regions",
        "service_slug": "amazon-eks",
        "type": "containers",
        "feature_type": "region-expansion",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=6)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/eks-auto-mode-region-expansion/",
        "raw_description": "Amazon EKS Auto Mode is now available in 10 additional AWS regions, bringing fully automated Kubernetes infrastructure management to more customers globally.",
        "summary": "EKS Auto Mode, which automates Kubernetes node provisioning, scaling, and upgrades, expands to 10 more AWS regions including ap-northeast-1, ap-southeast-1, eu-central-1, and others. EKS Auto Mode eliminates manual node group management by automatically selecting instance types, handling OS patching, and scaling based on pending pods. This expansion brings the total supported region count to 18. Existing EKS clusters in new regions can enable Auto Mode without cluster recreation.",
        "key_points": [
            "Now available in 18 total regions including new ap-northeast-1 and eu-central-1",
            "Automates node selection, patching, and Karpenter-based scaling",
            "Enable on existing clusters via eksctl or AWS Console without downtime"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-007-cloudwatch-ai-insights",
        "title": "Amazon CloudWatch introduces AI-powered anomaly detection for application logs",
        "service_slug": "amazon-cloudwatch",
        "type": "management-governance",
        "feature_type": "new-feature",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/cloudwatch-ai-anomaly-detection-logs/",
        "raw_description": "Amazon CloudWatch now offers AI-powered anomaly detection for application logs, automatically identifying unusual patterns without requiring manual threshold configuration.",
        "summary": "CloudWatch Log Anomaly Detection uses ML to identify unusual patterns in application logs without manual baseline configuration. The feature automatically learns normal log patterns and surfaces deviations in a new Anomalies tab in CloudWatch Logs Insights. Anomalies are classified by severity and include sample log lines and first/last occurrence timestamps. Costs $0.10 per GB of analyzed log data. Supports CloudWatch Logs groups; integration with CloudWatch Alarms for automated alerting coming Q3 2026.",
        "key_points": [
            "Zero-config ML baseline learns from 2+ weeks of log history automatically",
            "Anomalies surfaced in new CloudWatch Logs Insights Anomalies tab",
            "Priced at $0.10 per GB analyzed; CloudWatch Alarms integration in Q3 2026"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-008-dynamodb-price-reduction",
        "title": "Amazon DynamoDB reduces on-demand read/write prices by 20% in all regions",
        "service_slug": "amazon-dynamodb",
        "type": "databases",
        "feature_type": "price-change",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/dynamodb-on-demand-price-reduction/",
        "raw_description": "AWS announces a 20% price reduction for Amazon DynamoDB on-demand read and write request units across all commercial AWS regions, effective immediately.",
        "summary": "AWS reduces DynamoDB on-demand pricing by 20% for both read request units (RRUs) and write request units (WRUs) across all commercial regions, effective immediately. The new pricing brings WRUs to $1.00 per million and RRUs to $0.20 per million in us-east-1. Reserved capacity pricing is unchanged. This is the third DynamoDB price reduction in four years. Existing on-demand tables automatically benefit — no configuration changes required.",
        "key_points": [
            "20% price reduction for on-demand WRUs: now $1.00/million in us-east-1",
            "20% price reduction for on-demand RRUs: now $0.20/million in us-east-1",
            "Applies automatically to all existing on-demand tables with no action needed"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-009-bedrock-agents-code-interpreter",
        "title": "Amazon Bedrock Agents launches code interpretation capability in preview",
        "service_slug": "amazon-bedrock",
        "type": "ai-ml",
        "feature_type": "preview",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=12)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/bedrock-agents-code-interpreter-preview/",
        "raw_description": "Amazon Bedrock Agents now supports a built-in code interpretation action group in preview, allowing agents to write and execute Python code in a sandboxed environment to solve analytical tasks.",
        "summary": "Bedrock Agents Code Interpreter (preview) lets agents write and execute Python 3.11 in a sandboxed container to handle data analysis, math, and chart generation tasks. The sandbox is ephemeral per-session and supports pandas, numpy, matplotlib, and scipy. Agents can process uploaded CSV/JSON files, generate charts returned as base64 images, and perform multi-step analytical reasoning. Execution timeout is 30 seconds per code block. Available in us-east-1 and us-west-2 during preview; no additional charges beyond Bedrock token costs.",
        "key_points": [
            "Sandboxed Python 3.11 execution with pandas, numpy, matplotlib, scipy pre-installed",
            "Agents can analyze uploaded CSV/JSON and return generated charts as images",
            "30-second execution timeout per code block; session-ephemeral sandbox"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-010-sagemaker-deprecation",
        "title": "Amazon SageMaker Studio Classic reaches end-of-support on September 1, 2026",
        "service_slug": "amazon-sagemaker",
        "type": "ai-ml",
        "feature_type": "deprecation",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/sagemaker-studio-classic-end-of-support/",
        "raw_description": "Amazon SageMaker Studio Classic will reach end-of-support on September 1, 2026. Customers should migrate to SageMaker Studio (the new experience) before this date.",
        "summary": "Amazon SageMaker Studio Classic (the original JupyterServer-based IDE experience) will reach end-of-support on September 1, 2026. After this date, Classic domains will be automatically migrated to the new SageMaker Studio experience. AWS provides a migration guide and automated migration tool via the Console and CLI. The new Studio experience offers improved performance, faster startup times, and native integration with SageMaker Unified Studio. Customers have approximately 5 months to complete migration.",
        "key_points": [
            "End-of-support date: September 1, 2026 — automatic migration after this date",
            "New SageMaker Studio offers faster startup and SageMaker Unified Studio integration",
            "Migration guide and automated migration tool available at docs.aws.amazon.com/sagemaker/studio-migration"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-011-vpc-lattice-grpc",
        "title": "Amazon VPC Lattice adds gRPC protocol support for service-to-service communication",
        "service_slug": "amazon-vpc-lattice",
        "type": "networking-content-delivery",
        "feature_type": "new-feature",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=15)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/vpc-lattice-grpc-support/",
        "raw_description": "Amazon VPC Lattice now supports gRPC protocol for service-to-service communication, enabling microservices using gRPC to leverage Lattice's built-in auth, observability, and traffic management.",
        "summary": "VPC Lattice extends its service mesh capabilities to gRPC, the high-performance RPC framework. Teams running microservices with gRPC can now register them as VPC Lattice target groups and leverage built-in mTLS, IAM auth policies, and CloudWatch metrics without modifying application code. gRPC streaming (unary, server-streaming, client-streaming, bidirectional) is all supported. VPC Lattice handles TLS termination at the service network layer. Available in all regions where VPC Lattice is supported.",
        "key_points": [
            "All gRPC streaming modes supported: unary, server, client, and bidirectional",
            "IAM auth policies and CloudWatch metrics work identically to HTTP/2 services",
            "TLS termination handled by VPC Lattice — no cert management in application pods"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    {
        "guid": "mock-012-step-functions-ai-integration",
        "title": "AWS Step Functions integrates with Amazon Bedrock for multi-step AI workflow orchestration",
        "service_slug": "aws-step-functions",
        "type": "serverless",
        "feature_type": "integration",
        "pub_date": (datetime.now(timezone.utc) - timedelta(days=18)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "link": "https://aws.amazon.com/about-aws/whats-new/2026/04/step-functions-bedrock-integration/",
        "raw_description": "AWS Step Functions now offers native integration with Amazon Bedrock, allowing workflows to invoke Bedrock models, agents, and knowledge bases as first-class state machine states.",
        "summary": "Step Functions adds native Bedrock integration with three new state types: InvokeModel, InvokeAgent, and RetrieveAndGenerate. Engineers can build multi-step AI pipelines (e.g., classify → retrieve → summarize → store) using visual ASL without Lambda intermediary functions. The integration supports synchronous and asynchronous invocations, with built-in retry and error handling. Outputs from Bedrock states are automatically parsed as JSON and available to downstream states. Available in all regions where both services are supported.",
        "key_points": [
            "Three new state types: bedrock:InvokeModel, bedrock:InvokeAgent, bedrock:RetrieveAndGenerate",
            "Eliminates Lambda glue code for Bedrock calls in AI orchestration pipelines",
            "Full Step Functions error handling, retry, and distributed tracing apply to Bedrock states"
        ],
        "status": "summarized",
        "summarized_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
]


def load_mock_data(table_name: str, region: str, dry_run: bool = False):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    print(f"Loading {len(MOCK_FEATURES)} mock features into {table_name} ({region})")
    if dry_run:
        print("[DRY RUN] No data will be written.")
        for f in MOCK_FEATURES:
            print(f"  - {f['guid']}: {f['title'][:60]}...")
        return

    success = 0
    skipped = 0
    for feature in MOCK_FEATURES:
        resp = table.get_item(Key={'guid': feature['guid']}, ProjectionExpression='guid')
        if 'Item' in resp:
            print(f"  SKIP (exists): {feature['guid']}")
            skipped += 1
            continue

        table.put_item(Item=feature)
        print(f"  OK: {feature['guid']}")
        success += 1

    print(f"\nDone: {success} inserted, {skipped} skipped (already exist)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load mock data into DynamoDB')
    parser.add_argument('--table', default='aws-features', help='DynamoDB table name')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--dry-run', action='store_true', help='Print items without writing')
    args = parser.parse_args()

    try:
        load_mock_data(args.table, args.region, dry_run=args.dry_run)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
