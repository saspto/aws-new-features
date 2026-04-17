#!/usr/bin/env bash
set -euo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
# Note: SSM params use /app/features/ prefix (not /aws-features/ — reserved by AWS)
ENVIRONMENT="${ENVIRONMENT:-dev}"
STACK_NAME="aws-features-tracker-${ENVIRONMENT}"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
DEPLOY_BUCKET="aws-sam-deploy-${ACCOUNT_ID}-${AWS_REGION}"

echo "==> Deploying stack: ${STACK_NAME} in ${AWS_REGION}"
echo "==> Account: ${ACCOUNT_ID}"

# Create deploy bucket if it doesn't exist
if ! aws s3api head-bucket --bucket "${DEPLOY_BUCKET}" 2>/dev/null; then
  echo "==> Creating SAM deploy bucket: ${DEPLOY_BUCKET}"
  if [ "${AWS_REGION}" = "us-east-1" ]; then
    aws s3api create-bucket --bucket "${DEPLOY_BUCKET}" --region "${AWS_REGION}"
  else
    aws s3api create-bucket --bucket "${DEPLOY_BUCKET}" --region "${AWS_REGION}" \
      --create-bucket-configuration LocationConstraint="${AWS_REGION}"
  fi
fi

# Build
echo "==> Building SAM application..."
sam build --template infrastructure/template.yaml --build-dir .aws-sam/build

# Deploy
echo "==> Deploying SAM stack..."
sam deploy \
  --template-file .aws-sam/build/template.yaml \
  --stack-name "${STACK_NAME}" \
  --s3-bucket "${DEPLOY_BUCKET}" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment="${ENVIRONMENT}" \
  --region "${AWS_REGION}" \
  --no-fail-on-empty-changeset

# Capture outputs
echo "==> Capturing stack outputs..."
CF_URL=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" \
  --output text --region "${AWS_REGION}")

API_URL=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiGatewayURL'].OutputValue" \
  --output text --region "${AWS_REGION}")

FRONTEND_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendBucketName'].OutputValue" \
  --output text --region "${AWS_REGION}")

echo "==> CloudFront URL: ${CF_URL}"
echo "==> API URL: ${API_URL}"
echo "==> Frontend Bucket: ${FRONTEND_BUCKET}"

# Build frontend
echo "==> Building React frontend..."
cd frontend
npm ci
VITE_API_BASE_URL="" npm run build
cd ..

# Sync to S3
echo "==> Uploading frontend to S3..."
aws s3 sync frontend/dist/ "s3://${FRONTEND_BUCKET}/" \
  --delete \
  --cache-control "public, max-age=31536000, immutable" \
  --exclude "index.html"

aws s3 cp frontend/dist/index.html "s3://${FRONTEND_BUCKET}/index.html" \
  --cache-control "no-cache, no-store, must-revalidate" \
  --content-type "text/html"

echo ""
echo "======================================"
echo " Deployment complete!"
echo " CloudFront URL: ${CF_URL}"
echo "======================================"
