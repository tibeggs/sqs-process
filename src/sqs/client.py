import boto3
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import AWS_REGION, SQS_QUEUE_URL

class SQSClient:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION
        )
        self.queue_url = SQS_QUEUE_URL

    def receive_message(self):
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
            AttributeNames=[
                        'SentTimestamp'
                    ]
        )
        return response.get('Messages', [])

    def delete_message(self, receipt_handle):
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )