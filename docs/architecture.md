# Architecture — Compliance Automator

This document describes the production architecture the repo deploys via Terraform (or CDK). The companion case-study article on [creativeminds.dev/blog](https://creativeminds.dev/blog/compliance-automator-case-study) explains the engineering decisions; this doc is the operator's reference.

## System overview

The compliance automator is a Strands-on-Bedrock agent running inside the customer's VPC (per the [air-gapped Bedrock pattern](https://creativeminds.dev/blog/air-gapped-llm-deployments-aws-bedrock)). It takes a regulator-style query as input, retrieves relevant chunks from the regulatory corpus and the customer's evidence sources, reasons over them with Claude Sonnet, and produces a structured evidence pack with citations.

The four-layer Bedrock agent architecture from the [Foundations article](https://creativeminds.dev/blog/building-ai-agents-on-amazon-bedrock-foundations) applies directly:

1. **Model** — Claude Sonnet 4.6 (pinned, reasoning); Claude Haiku 4.5 (pinned, router); Cohere Embed v3 (embeddings); Cohere Rerank v3 (re-ranking).
2. **Tools** — Lambda functions exposed as Action Groups with OpenAPI schemas: `query_cloudtrail`, `query_security_lake`, `retrieve_regulation`, `generate_evidence_pack`, `format_pdf`.
3. **Memory** — Knowledge Base of regulatory texts + customer policy documents; short-term sliding-window conversation manager for multi-turn queries.
4. **Orchestration** — Strands agent loop on AgentCore Runtime, with hooks for audit, steering handlers for safety, `event.interrupt()` gates on any tool that emits or modifies persistent artefacts.

## Component map

| Component | Role | AWS resource |
|---|---|---|
| **Query intake** | Receives the regulator-style query | API Gateway + WAF (REST) or direct CLI |
| **Router** | Decides Haiku-tier vs Sonnet-tier processing | `agent.pipeline.classify_query` (Lambda) |
| **Agent runtime** | Runs the Strands loop | AgentCore Runtime (managed) |
| **Knowledge Base** | Regulatory corpus + customer policies | Bedrock Knowledge Base + OpenSearch Serverless |
| **Action tools** | CloudTrail/Security Lake queries, evidence-pack gen | Lambda + Powertools |
| **Guardrails** | PII filter (BVN, NIN), denied-topic, grounding | Bedrock Guardrails (referenced by ID) |
| **Audit trail** | CloudTrail data events + model invocation logs | S3 + KMS CMK + Object Lock |
| **Observability** | Metrics, traces, alarms | CloudWatch + X-Ray |

## Deployment layout

The architecture follows the [air-gapped Bedrock pattern](https://creativeminds.dev/blog/air-gapped-llm-deployments-aws-bedrock) end-to-end:

- VPC with private subnets only, no IGW on workload subnets
- VPC endpoints for `bedrock-runtime`, `bedrock-agent-runtime`, KMS, S3, Secrets, CloudWatch, STS
- KMS CMK on every encrypted resource, scoped key policies
- IAM Identity Center federation for human access; workload identities via IRSA/IAM Roles
- Cross-account audit forwarding to a separate Security OU account

## What's not in this repo

Things that are intentionally out of scope:

- The customer's actual data — replaced by synthetic CloudTrail and Security Lake samples
- Production-grade web UI — the side-by-side comparison portal demo is in `examples/web/` (forthcoming) but is a reference, not a hardened product
- The customer-specific evidence-pack PDF template — the version in `examples/templates/` is the cmdev reference; production deployments customise this per customer brand
- Multi-region failover — the deployment is single-region; for production deployments cmdev adds the multi-region pattern from the [AWS-for-banks series](https://creativeminds.dev/blog/aws-architecture-nigerian-banks)

## Architecture Decision Records

See `docs/adrs/` for the documented decisions. Each ADR captures a specific architectural choice, the alternatives considered, and the reasoning. Initial set:

- ADR-001: Strands + AgentCore over LangChain or custom loop
- ADR-002: OpenSearch Serverless for the Knowledge Base vector store
- ADR-003: Two-pass SME golden-set labelling protocol
- ADR-004: Cross-account audit log forwarding
- ADR-005: Per-purpose KMS CMKs over single workload key

## See also

- [Companion case study article](https://creativeminds.dev/blog/compliance-automator-case-study) (forthcoming)
- [Bedrock for Production AI series — 8 parts](https://creativeminds.dev/blog/building-ai-agents-on-amazon-bedrock-foundations)
- [Air-Gapped LLM Deployments](https://creativeminds.dev/blog/air-gapped-llm-deployments-aws-bedrock)
- [Custom LLM Evaluation Frameworks](https://creativeminds.dev/blog/custom-evaluation-frameworks-enterprise-llms)
