# Terraform deployment — Compliance Automator

This directory contains the production Terraform that stands up the full compliance-automator pattern in a fresh AWS account. The deployment is single-region; multi-region failover is a cmdev engagement add-on.

## Prerequisites

- Terraform ≥ 1.9
- AWS credentials with sufficient permissions to create VPC, IAM, Bedrock, OpenSearch Serverless, Lambda, S3, KMS resources
- Bedrock model access enabled (see [/docs/local-aws-setup.md](../docs/local-aws-setup.md))

## Layout

```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── modules/
│   ├── network/             # VPC + private subnets + VPC endpoints
│   ├── kms/                 # CMKs (per-purpose)
│   ├── knowledge-base/      # Bedrock KB + OpenSearch Serverless
│   ├── guardrail/           # Bedrock Guardrail config
│   ├── action-tools/        # Lambda functions + IAM roles
│   ├── agent-runtime/       # AgentCore runtime config
│   └── observability/       # CloudTrail, model invocation logs, alarms
└── envs/
    ├── dev.tfvars.example
    └── prod.tfvars.example
```

## Deploy

```bash
# Initialise
terraform init

# Plan against the dev configuration
terraform plan -var-file=envs/dev.tfvars

# Apply
terraform apply -var-file=envs/dev.tfvars
```

## Modules — status

| Module | Status | Reference |
|---|---|---|
| `network` | Scaffolded | [Air-gapped Bedrock article](https://creativeminds.dev/blog/air-gapped-llm-deployments-aws-bedrock) |
| `kms` | Scaffolded | Same |
| `knowledge-base` | Scaffolded | [RAG article](https://creativeminds.dev/blog/rag-with-bedrock-knowledge-bases) |
| `guardrail` | Scaffolded | [Security & Observability article](https://creativeminds.dev/blog/security-guardrails-observability-bedrock) |
| `action-tools` | Scaffolded | [Step Functions + Bedrock article](https://creativeminds.dev/blog/multi-step-workflows-step-functions-bedrock) |
| `agent-runtime` | Scaffolded | [Open-source Agent Frameworks article](https://creativeminds.dev/blog/open-source-agent-frameworks-on-bedrock) |
| `observability` | Scaffolded | [Security & Observability article](https://creativeminds.dev/blog/security-guardrails-observability-bedrock) |

The CDK directory ships an equivalent set of constructs. Either path produces the same deployed state.
