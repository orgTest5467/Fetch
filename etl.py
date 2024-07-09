import boto3
import psycopg2
from hashlib import sha256
import json

def mask_pii(value):
    # SHA-256 hash function to mask PII consistently
    return sha256(value.encode('utf-8')).hexdigest()

def verify_pii(plaintext_value, hashed_value):
    # Hash the plaintext value to compare with the stored hashed value
    return mask_pii(plaintext_value) == hashed_value

def fetch_messages():
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
    queue_url = sqs.get_queue_url(QueueName='my-app-queue')['QueueUrl']

    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    ).get('Messages', [])

    return messages

def transform_data(message):
    body = json.loads(message['Body'])
    # Masking masked_device_id and masked_ip fields using the mask_pii function
    body['masked_device_id'] = mask_pii(body['masked_device_id'])
    body['masked_ip'] = mask_pii(body['masked_ip'])
    return body

def write_to_postgres(records):
    conn = psycopg2.connect(
        dbname='logins',  # Ensure this matches your database name
        user='postgres',  # Updated username
        password='postgres',  # Updated password
        host='localhost'
    )
    cur = conn.cursor()
    for record in records:
        cur.execute("""
            INSERT INTO login_user (user_id, devide_type, masked_ip, masked_device_id, Locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (record['user_id'], record['devide_type'], record['masked_ip'], record['masked_device_id'], record['Locale'], record['app_version'], record['create_date']))
    conn.commit()
    cur.close()
    conn.close()

def main():
    messages = fetch_messages()
    records = [transform_data(msg) for msg in messages]
    write_to_postgres(records)

    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
    queue_url = sqs.get_queue_url(QueueName='my-app-queue')['QueueUrl']
    for message in messages:
        print(message)
        sqs.delete_message(QueueUrl=queue_url, Recemasked_iptHandle=message['ReceiptHandle'])

    # retrieve_data()
    # print("bye")
    

if __name__ == '__main__':
    main()


