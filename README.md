# Cloud-Native Automated Incident Response (SOAR Engine)

[![AWS](https://img.shields.io/badge/AWS-Step Functions-orange?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/step-functions/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An event-driven Security Orchestration, Automation, and Response (SOAR) framework deployed on AWS using Step Functions, Lambda handlers, EventBridge, and AWS GuardDuty.

## 🏗️ Architecture & Remediation Workflow

```text
[ AWS GuardDuty Threat Finding ]
               ↓
               ↓
   [ Amazon EventBridge Rule ]
               ↓
               ↓
[ AWS Step Functions State Machine ]
               ↓
     +---------+---------+
     ↓         ↓         ↓
[ Lambda 1 ] [ Lambda 2 ] [ Lambda 3 ]
 (IAM Revoke) (EC2 Isolate) (WAF Block)
     ↓         ↓         ↓
     +---------+---------+
               ↓
    [ Amazon SNS Alerting ]
```

## 🚀 Automated Remediation Actions

### IAM Session Revocation (`lambda/revoke_iam.py`)
Attaches an inline DenyAll policy to compromised IAM user accounts to immediately block active session credentials.

### EC2 Network Isolation (`lambda/isolate_ec2.py`)
Replaces existing Security Groups with a zero-access Quarantine Security Group (sg-quarantine) to isolate compromised compute nodes.

### AWS WAF IP Blocking (`lambda/block_waf_ip.py`)
Appends malicious source IPs directly to an AWS WAF v2 IP Set to drop incoming web traffic at the edge.

## 📁 Repository Structure

```
aws-soar-incident-response/
├── iac/
│   └── statemachine/
│       └── soar_workflow.asl.json   # Step Functions State Machine Definition
├── lambda/
│   ├── revoke_iam.py               # IAM Session Revocation Handler
│   ├── isolate_ec2.py              # EC2 Quarantine Handler
│   └── block_waf_ip.py             # WAF IP Block Handler
├── events/
│   ├── guardduty_iam_threat.json   # Simulated IAM Threat Payload
│   ├── guardduty_ec2_threat.json   # Simulated EC2 Threat Payload
│   └── guardduty_waf_threat.json   # Simulated WAF Threat Payload
├── tests/
│   └── test_remediation.py         # Event Parser & Remediation Test Suite
└── README.md
```

## 🧪 Local Test Verification

Execute the test suite to validate GuardDuty JSON schema parsing across all threat vectors:

```bash
python tests/test_remediation.py
```

## 📋 Prerequisites

- AWS Account with appropriate IAM permissions
- AWS GuardDuty enabled
- Python 3.8+
- AWS CLI configured with appropriate credentials

## 🔧 Installation & Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aws-soar-incident-response
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Deploy AWS resources**
   ```bash
   # Deploy Step Functions State Machine
   aws stepfunctions create-state-machine --definition file://iac/statemachine/soar_workflow.asl.json --name "SOAR-Workflow"
   
   # Deploy Lambda functions
   aws lambda create-function --function-name "revoke-iam" --runtime python3.8 --handler lambda/revoke_iam.handler --zip-file fileb://lambda/revoke_iam.zip
   ```

4. **Configure EventBridge rules**
   ```bash
   aws events put-rule --name "GuardDuty-Threat-Detection" --event-pattern file://events/guardduty_pattern.json
   ```

## 🔒 Security Considerations

- Ensure least privilege IAM policies for Lambda execution roles
- Implement proper SNS topic encryption for alert notifications
- Use AWS KMS for sensitive data encryption
- Enable CloudTrail logging for audit trails

## 📊 Monitoring & Alerts

- CloudWatch Alarms for Step Functions execution failures
- SNS notifications for remediation actions
- CloudWatch Logs for Lambda function debugging

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review AWS GuardDuty and Step Functions documentation