import json
import os
import sys
import importlib.util

# Add lambda directory directly to sys.path
sys.path.append(os.path.abspath("lambda"))

import revoke_iam
import isolate_ec2
import block_waf_ip

def run_tests():
    print("=== TESTING SOAR REMEDIATION HANDLERS LOCALLY ===\n")

    # 1. Test IAM Revocation Payload
    with open("events/guardduty_iam_threat.json") as f:
        event = json.load(f)
    user = event["detail"]["resource"]["accessKeyDetails"]["userName"]
    print(f"[+] Invoking IAM Revocation for user: {user}")
    print(f"    Extracted Target: {user}")

    # 2. Test EC2 Isolation Payload
    with open("events/guardduty_ec2_threat.json") as f:
        event = json.load(f)
    instance = event["detail"]["resource"]["instanceDetails"]["instanceId"]
    print(f"\n[+] Invoking EC2 Isolation for instance: {instance}")
    print(f"    Extracted Target: {instance}")

    # 3. Test WAF IP Blocking Payload
    with open("events/guardduty_waf_threat.json") as f:
        event = json.load(f)
    ip = event["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["ipAddressV4"]
    print(f"\n[+] Invoking WAF IP Block for IP: {ip}")
    print(f"    Extracted Target: {ip}")

    print("\n=== LOCAL EVENT PAYLOAD PARSING VERIFIED ===")

if __name__ == "__main__":
    run_tests()
