import json
import logging
import os
import uuid
from datetime import datetime
# import pkg_resources
# from jinja2 import Environment, FileSystemLoader
# from weasyprint import HTML
import boto3
dynamodb = boto3.resource('dynamodb')

TAX_PERCENTAGE = 13


def create(event, context):

    data = json.loads(event['body'])
    if (
        'date' not in data and
        'cost' not in data and
        'description' not in data and
        'customerID' not in data
    ):
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    timestamp = str(datetime.utcnow())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    tax = float(data['cost']) * (TAX_PERCENTAGE / 100.0)

    item = {
        'id': str(uuid.uuid1()),
        'date': data['date'],
        'description': data['description'],
        'customerID': data['customerID'],
        'cost': data['cost'],
        'tax': str(tax),
        'total': str(float(data['cost']) + tax),
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    s3_url = create_invoice(item)
    item['pdf_location'] = s3_url

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response


def create_invoice(item):
    """Create invoice for customer."""
    # TODO: Generate invoice locally. Upload to S3. Get presigned URL.

    return "https://s3_location/invoice.pdf"
