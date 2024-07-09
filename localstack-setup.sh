#!/bin/sh
echo "Initializing localstack s3"

awslocal s3 mb s3://incircl
awslocal sqs create-queue --queue-name my-app-queue
awslocal --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/my-app-queue  --message-body '
{
        "user_id": "user_12345",
        "devide_type": "iOS",
        "masked_ip": "192.168.1.1",
        "masked_device_id": "device_abc123",
        "Locale": "en_US",
        "app_version": 12,
        "create_date": "2023-07-01"
    }'

