import boto3
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    iam_client = boto3.client("iam")
    username = event.get("IAMUserName", "UNKNOWN_USER")
    logger.info(f"Initiating session revocation for IAM User: {username}")
    
    if username == "UNKNOWN_USER":
        return {"statusCode": 400, "body": json.dumps("No valid IAM user provided.")}

    try:
        deny_policy = {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}]
        }
        iam_client.put_user_policy(
            UserName=username,
            PolicyName="SOAR-AutoRemediation-DenyAll",
            PolicyDocument=json.dumps(deny_policy)
        )
        return {
            "statusCode": 200,
            "status": "SUCCESS",
            "remediation": "IAM_SESSIONS_REVOKED",
            "targetUser": username,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to revoke user sessions: {str(e)}")
        raise e
