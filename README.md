# Compliance Automator

> An open-source AI agent on Amazon Bedrock that turns regulator-style queries into audit-grade evidence packs — with citations to source events, mapped against NDPA 2023, CBN CSAT, EU NIS2 Article 21, and NIST SP 800-53.

**Companion to the [Case Study article on creativeminds.dev](https://creativeminds.dev/blog/compliance-automator-case-study).** Built and open-sourced by [CreativeMinds Development (cmdev)](https://creativeminds.dev).

---

## What this is

A side-by-side comparison portal for compliance officers and CISOs at regulated enterprises. Drop a draft policy, contract, or operational artefact on the left. The agent highlights non-compliant clauses on the right, with deep-links to the exact section of the official government regulation it is being checked against. Returns a structured evidence pack the compliance team can hand to a regulator.

Built on:

- **Amazon Bedrock** — pinned Claude Sonnet 4.6 for reasoning, Claude Haiku 4.5 for routing
- **Cohere Embed v3** — for regulatory-corpus retrieval embeddings
- **Amazon OpenSearch Serverless** — vector store with hybrid search and re-ranking
- **Strands Agents SDK** + **AgentCore Runtime** — the open-source agent harness
- **AWS Lambda + Powertools** — tool implementations with OpenAPI schemas
- **Bedrock Guardrails** — PII filters (NIN, BVN regex), denied-topic policies, contextual grounding

Compliance scope shipped in this reference: **NDPA 2023** (Nigeria) · **CBN CSAT** (Nigeria, banking) · **EU NIS2 Article 21** · **NIST SP 800-53** controls subset.

## Quickstart — run it locally

The reference deployment runs on AWS, but the full pipeline can be exercised locally against synthetic data and the public regulatory corpus shipped in this repo.

```bash
# 1. Clone
git clone https://github.com/Samueladewole/compliance-automator
cd compliance-automator

# 2. Python environment (uv recommended; pip works too)
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# 3. Configure AWS credentials (Bedrock requires a real account; see /docs/local-aws-setup.md)
export AWS_REGION=eu-central-1
export BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-6-20251022
aws configure sso  # or use any other auth path your team uses

# 4. Run the local agent against an example query
python -m agent.cli "Show me all privileged-access changes in production for the past 90 days, with the approval trail, mapped to NDPA Section 39."

# 5. Run the evaluation harness against the golden set
make eval
```

Expected output for step 4: an evidence pack JSON with citations to specific events in the synthetic CloudTrail data (`/data/synthetic/cloudtrail-events.jsonl`), mapped against the NDPA regulatory text (`/data/regulations/ndpa-2023.md`).

## Repository structure

```
compliance-automator/
├── agent/                  # Strands-on-Bedrock agent — Python
│   ├── cli.py              # local CLI entry point
│   ├── tools/              # action tools (CloudTrail query, evidence-pack gen, etc.)
│   ├── hooks/              # audit + steering hooks
│   ├── prompts/            # version-controlled system prompts
│   └── eval/               # golden set + LLM-as-judge metrics
├── terraform/              # Production deployment — AWS Bedrock, KB, OpenSearch Serverless, etc.
│   ├── main.tf
│   ├── modules/
│   └── README.md
├── cdk/                    # Parallel CDK implementation — TypeScript
│   ├── lib/
│   ├── bin/
│   └── README.md
├── eval/                   # Top-level eval harness — runs over the deployed pipeline
│   ├── golden_set.jsonl
│   ├── run_eval.py
│   └── results/
├── examples/               # End-to-end usage examples
│   ├── ndpa_evidence_request.md
│   ├── cbn_csat_quarterly.md
│   └── nis2_article_21_mapping.md
├── docs/
│   ├── architecture.md     # the system, end-to-end
│   ├── adrs/               # architecture decision records
│   ├── local-aws-setup.md
│   └── what-this-taught-us.md  # the "Lessons" section from the article
└── data/
    ├── regulations/        # public regulatory texts: NDPA, CBN CSAT, NIS2, NIST 800-53
    └── synthetic/          # synthetic CloudTrail + IAM data for local runs
```

## Two infrastructure flavours — Terraform and CDK

Both deploy the same set of resources to the same final state. The choice between them is a team preference, not an architectural difference.

| Resource | Terraform module | CDK construct |
|---|---|---|
| VPC + private subnets + VPC endpoints | `terraform/modules/network` | `cdk/lib/network-stack.ts` |
| KMS CMK + key policies | `terraform/modules/kms` | `cdk/lib/kms-stack.ts` |
| OpenSearch Serverless KB vector store | `terraform/modules/knowledge-base` | `cdk/lib/knowledge-base-stack.ts` |
| Bedrock Guardrail | `terraform/modules/guardrail` | `cdk/lib/guardrail-stack.ts` |
| Lambda action tools | `terraform/modules/action-tools` | `cdk/lib/action-tools-stack.ts` |
| AgentCore runtime | `terraform/modules/agent-runtime` | `cdk/lib/agent-runtime-stack.ts` |
| Observability (CloudTrail, model invocation logs) | `terraform/modules/observability` | `cdk/lib/observability-stack.ts` |

Deploy from a fresh AWS account:

```bash
# Terraform
cd terraform/
terraform init && terraform apply

# OR CDK
cd cdk/
npm install && npx cdk bootstrap && npx cdk deploy --all
```

## What's in the repo at this stage

This repo is the **public reference implementation** for the cmdev compliance-automator pattern. Current status:

- ✅ Repository structure scaffolded
- ✅ Sample regulatory corpus (NDPA 2023, NIS2 Article 21 — public texts)
- 🚧 Strands agent — in progress
- 🚧 Terraform modules — in progress
- 🚧 CDK constructs — in progress
- 🚧 Evaluation harness — in progress
- 🚧 Demo web app (side-by-side comparison portal) — in progress

Target ship: end of June 2026. Watch this repo or follow [creativeminds.dev/blog](https://creativeminds.dev/blog) for the announcement.

## What this teaches you about enterprise scaling

Every architectural decision in this repo is documented in [`docs/what-this-taught-us.md`](docs/what-this-taught-us.md) as it ships. The decisions:

- Why we chose Strands + AgentCore over LangChain or building a custom agent loop
- Why the same architecture sits inside the customer's VPC (air-gapped), not in a multi-tenant SaaS
- Why the evidence pack is a structured artefact, not a chatbot transcript
- Why the eval harness is shipped alongside the agent, not as an afterthought
- The friction points we hit and engineered past

If you are a CISO or compliance officer evaluating production AI for regulated work, the architecture decisions documented here are the ones we would walk through in a consulting engagement. The repo is the long version; the [cmdev case study article](https://creativeminds.dev/blog/compliance-automator-case-study) is the short one.

## Engaging with cmdev

This is one of several reference architectures CreativeMinds Development (cmdev) ships for regulated enterprises. We deliver production AI for banking, energy, healthcare, and critical-infrastructure customers across Africa and the EU.

- **Email:** info@creativeminds.dev
- **Web:** [creativeminds.dev](https://creativeminds.dev)
- **Companion architecture series:** [Bedrock for Production AI](https://creativeminds.dev/blog/building-ai-agents-on-amazon-bedrock-foundations), [Air-Gapped LLM Deployments](https://creativeminds.dev/blog/air-gapped-llm-deployments-aws-bedrock), [Custom LLM Evaluation Frameworks](https://creativeminds.dev/blog/custom-evaluation-frameworks-enterprise-llms)

## License

MIT — see [LICENSE](LICENSE). Use it, fork it, deploy it for your customers. If you build something interesting on top of it, we would love to hear about it.

## Authors

- **Mayowa A.** — CTO, CreativeMinds Development · [github.com/MayowaAdewole](#)
- **Samuel A.** — Co-founder, CreativeMinds Development · [github.com/Samueladewole](https://github.com/Samueladewole)

---

*Built by [CreativeMinds Development](https://creativeminds.dev). Open source · MIT licensed · contributions welcome.*
