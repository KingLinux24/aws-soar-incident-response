import boto3
import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

IP_SET_ID = os.environ.get("WAF_IP_SET_ID", "00000000-0000-0000-0000-000000000000")
IP_SET_NAME = os.environ.get("WAF_IP_SET_NAME", "SOAR-Blocked-Attacker-IPs")
SCOPE = os.environ.get("WAF_SCOPE", "REGIONAL")

def lambda_handler(event, context):
    waf_client = boto3.client("wafv2")
    attacker_ip = event.get("AttackerIP", "0.0.0.0")
    logger.info(f"Initiating WAF IP Block for IP: {attacker_ip}")

    if attacker_ip == "0.0.0.0":
        return {"statusCode": 400, "body": json.dumps("No valid IP address provided.")}

    try:
        response = waf_client.get_ip_set(Name=IP_SET_NAME, Scope=SCOPE, Id=IP_SET_ID)
        current_addresses = response["IPSet"]["Addresses"]
        lock_token = response["LockToken"]
        
        formatted_ip = f"{attacker_ip}/32"
        if formatted_ip not in current_addresses:
            current_addresses.append(formatted_ip)
            waf_client.update_ip_set(
                Name=IP_SET_NAME, Scope=SCOPE, Id=IP_SET_ID,
                Addresses=current_addresses, LockToken=lock_token
            )
        return {
            "statusCode": 200,
            "status": "SUCCESS",
            "remediation": "WAF_IP_BLOCKED",
            "blockedIp": attacker_ip,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to apply WAF block rule: {str(e)}")
        raise e
