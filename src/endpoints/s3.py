import os
import json
import boto3
from src.core.response import return_success


def index(event: dict, context):
    records = event.get('Records', [])
    s3 = boto3.client('s3')
    source_bucket = os.environ.get('INCOMING_BUCKET_NAME')
    target_bucket = os.environ.get('PROCESSED_BUCKET_NAME')
    results = list()

    for record in records:
        item = record['s3']
        if item['bucket']['name'] != source_bucket:
            print("Bucket mismatch between %s and %s." % (
                source_bucket, item['bucket']['name']
            ))
            continue
        key = item['object']['key']
        copy_source = {
            'Bucket': source_bucket,
            'Key': key
        }
        try:
            s3.copy_object(Bucket=target_bucket, Key=key, CopySource=copy_source)
            results.append({
                'object': copy_source,
                'success': True
            })
            s3.delete_object(Bucket=source_bucket, Key=key)
        except Exception as e:
            print(str(e))
            results.append({
                'object': copy_source,
                'success': False,
                'msg': str(e)
            })
    return return_success(results)
