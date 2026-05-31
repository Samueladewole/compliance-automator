# CDK deployment — Compliance Automator

This directory contains the AWS CDK (TypeScript) deployment that stands up the same architecture as the [Terraform deployment](../terraform/README.md). Pick whichever IaC flavour fits your team — they produce equivalent results.

## Prerequisites

- Node.js ≥ 20
- AWS CDK v2 (installed via `npm install`)
- AWS credentials with sufficient permissions (see [/docs/local-aws-setup.md](../docs/local-aws-setup.md))

## Layout

```
cdk/
├── bin/
│   └── compliance-automator.ts       # CDK app entry point
├── lib/
│   ├── network-stack.ts              # VPC + endpoints
│   ├── kms-stack.ts                  # Per-purpose CMKs
│   ├── knowledge-base-stack.ts       # Bedrock KB + OpenSearch Serverless
│   ├── guardrail-stack.ts            # Bedrock Guardrail
│   ├── action-tools-stack.ts         # Lambda + IAM
│   ├── agent-runtime-stack.ts        # AgentCore runtime
│   └── observability-stack.ts        # CloudTrail + invocation logs
├── package.json
├── tsconfig.json
└── cdk.json
```

## Deploy

```bash
# Install
npm install

# Bootstrap once per account / region
npx cdk bootstrap

# Synth (review the templates)
npx cdk synth

# Deploy
npx cdk deploy --all
```

## Stacks — status

| Stack | Status |
|---|---|
| `NetworkStack` | Scaffolded |
| `KmsStack` | Scaffolded |
| `KnowledgeBaseStack` | Scaffolded |
| `GuardrailStack` | Scaffolded |
| `ActionToolsStack` | Scaffolded |
| `AgentRuntimeStack` | Scaffolded |
| `ObservabilityStack` | Scaffolded |

The Terraform directory ships an equivalent set of modules. Either path produces the same deployed state.
