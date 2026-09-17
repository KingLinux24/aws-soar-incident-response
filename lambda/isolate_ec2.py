import boto3
import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUARANTINE_SG_ID = os.environ.get("QUARANTINE_SG_ID", "sg-00000000000000000")

def lambda_handler(event, context):
    ec2_client = boto3.client("ec2")
    instance_id = event.get("InstanceId", "UNKNOWN_INSTANCE")
    logger.info(f"Initiating network isolation for EC2 Instance: {instance_id}")

    if instance_id == "UNKNOWN_INSTANCE":
        return {"statusCode": 400, "body": json.dumps("No valid Instance ID provided.")}

    try:
        ec2_client.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[QUARANTINE_SG_ID]
        )
        return {
            "statusCode": 200,
            "status": "SUCCESS",
            "remediation": "EC2_NETWORK_ISOLATED",
            "targetInstance": instance_id,
            "quarantineGroupId": QUARANTINE_SG_ID,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to isolate EC2 instance: {str(e)}")
        raise e
