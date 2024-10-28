import boto3
import time
import pprint as pp
from utils import get_gsi_status, wait_gsi_creating

TABLE_NAME = "dynamodb-stack-sample19A77B3F-LHABBZ9NVLXR"

ddb = boto3.resource("dynamodb")
table = ddb.Table(TABLE_NAME)

def put_items(data):
    for d in data:
        keys = list(d.keys())
        key_id = keys[0]
        keys.remove(key_id)

        for key in keys:
            if key == "TimeRange":
                item = {
                    "ID": d[key_id],
                    "DataType": key,
                    "DataValue": key,
                    "StartTime": d[key]["StartTime"],
                    "EndTime": d[key]["EndTime"]
                }
            else:
                item = {
                    "ID": d[key_id],
                    "DataType": key,
                    "DataValue": d[key]
                }
            table.put_item(Item=item)
        item = {
            "ID": d[key_id],
            "DataType": key_id,
            "DataValue": d[key_id]
        }
        table.put_item(Item=item)

events = [
    {
        "EventID": "E123",
        "EventName": "DynamoDB勉強会",
        "VenueID": "V32",
        "Date": "2024-03-14",
        "TimeRange": {"StartTime": "2024-03-14 10:00:00", "EndTime": "2024-03-14 12:00:00"},
        "Tag_#DynamoDB": "Tag_#DynamoDB",
        "Tag_#Serverless": "Tag_#Serverless",
    },
    {
        "EventID": "E456",
        "EventName": "サーバーレス勉強会",
        "VenueID": "V32",
        "Date": "2024-05-09",
        "TimeRange": {"StartTime": "2024-05-09 10:00:00", "EndTime": "2024-05-09 12:00:00"},
        "Tag_#Serverless": "Tag_#Serverless",
        "Tag_#Lambda": "Tag_#Lambda",
        "Tag_#Design": "Tag_#Design",
    }
]

venues = [
    {
        "VenueID": "V32",
        "VenueName": "Loft Tokyo",
        "VenueAddress": "目黒セントラルスクエア"
    }
]

put_items(events)
put_items(venues)

if get_gsi_status("GSI-2") != "ACTIVE":
    table.update(
        AttributeDefinitions=[
            {
                "AttributeName": "DataType",
                "AttributeType": "S"
            },
            {
                "AttributeName": "ID",
                "AttributeType": "S"
            },
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "GSI-2",
                    "KeySchema": [
                        {
                            "AttributeName": "DataType",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "ID",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "KEYS_ONLY",
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            }
        ]
    )

wait_gsi_creating("GSI-2")

if get_gsi_status("GSI-1") != "ACTIVE":
    table.update(
        AttributeDefinitions=[
            {
                "AttributeName": "DataValue",
                "AttributeType": "S"
            },
            {
                "AttributeName": "ID",
                "AttributeType": "S"
            },
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "GSI-1",
                    "KeySchema": [
                        {
                            "AttributeName": "DataValue",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "ID",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "KEYS_ONLY",
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            }
        ]
    )

wait_gsi_creating("GSI-1")

if get_gsi_status("GSI-3") != "ACTIVE":
    table.update(
        AttributeDefinitions=[
            {
                "AttributeName": "DataType",
                "AttributeType": "S"
            },
            {
                "AttributeName": "DataValue",
                "AttributeType": "S"
            },
            {
                "AttributeName": "StartTime",
                "AttributeType": "S"
            },
            {
                "AttributeName": "EndTime",
                "AttributeType": "S"
            },
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "GSI-3",
                    "KeySchema": [
                        {
                            "AttributeName": "DataType",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "DataValue",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "INCLUDE",
                        "NonKeyAttributes": ["StartTime", "EndTime"]
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            }
        ]
    )

wait_gsi_creating("GSI-3")