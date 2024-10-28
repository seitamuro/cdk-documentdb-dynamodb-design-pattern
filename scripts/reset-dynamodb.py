import boto3 
import pprint as p
from envs import TABLE_NAME
from utils import get_gsi_status, wait_gsi_deleting

ddb = boto3.resource("dynamodb")

def delete_all_items():
    table = ddb.Table(TABLE_NAME)
    response = table.scan()

    with table.batch_writer() as batch:
        for each in response["Items"]:
            batch.delete_item(
                Key={
                    "ID": each["ID"],
                    "DataType": each["DataType"]
                }
            )

delete_all_items()

table = ddb.Table(TABLE_NAME)

if get_gsi_status("GSI-1") == "ACTIVE":
    table.update(
        GlobalSecondaryIndexUpdates=[
            {
                "Delete": {
                    "IndexName": "GSI-1"
                }
            }
        ]
    )

wait_gsi_deleting("GSI-1")

if get_gsi_status("GSI-2") == "ACTIVE":
    table.update(
        GlobalSecondaryIndexUpdates=[
            {
                "Delete": {
                    "IndexName": "GSI-2"
                }
            }
        ]
    )

wait_gsi_deleting("GSI-2")