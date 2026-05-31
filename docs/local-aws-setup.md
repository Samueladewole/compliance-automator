# Local AWS setup

Running the compliance automator locally still requires real AWS credentials because the agent calls Amazon Bedrock for inference. This document walks through the minimum setup to exercise the pipeline against synthetic data shipped in the repo.

## Prerequisites

- An AWS account with Bedrock model access enabled for **Claude Sonnet 4.6** and **Claude Haiku 4.5** in `eu-central-1` (or your preferred region).
- A KMS Customer Managed Key in your account (the deployment creates one; for local-only runs you can use the default AWS managed key by setting `--kms-key default` on the CLI — not recommended for anything beyond local exploration).
- AWS CLI v2 installed and configured with credentials.

## Enable Bedrock model access

Bedrock models require explicit access approval before they can be invoked. From the AWS console:

1. Go to the Amazon Bedrock console
2. Navigate to **Model access**
3. Request access to:
   - `Anthropic Claude Sonnet 4.6`
   - `Anthropic Claude Haiku 4.5`
   - `Cohere Embed English v3`
   - `Cohere Rerank v3`
4. Approval is usually instant for Anthropic models; Cohere may take up to 24 hours.

## Configure credentials

Pick whichever auth flow your team uses. Two common patterns:

### Option A — IAM Identity Center (recommended for human use)

```bash
aws configure sso
# follow the prompts; this writes a profile to ~/.aws/config
export AWS_PROFILE=your-profile-name
aws sts get-caller-identity  # verify
```

### Option B — Long-lived IAM user credentials (lower friction for tinkering)

```bash
aws configure
# enter access key ID + secret + region (eu-central-1)
aws sts get-caller-identity  # verify
```

**Note:** in production we use Option A everywhere. Static credentials in `~/.aws/credentials` are a development convenience only.

## Required IAM permissions

The local user / role needs at minimum:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:Converse",
        "bedrock:Retrieve",
        "bedrock-runtime:InvokeModel",
        "bedrock-runtime:Converse"
      ],
      "Resource": [
        "arn:aws:bedrock:eu-central-1::foundation-model/anthropic.claude-sonnet-4-6-20251022",
        "arn:aws:bedrock:eu-central-1::foundation-model/anthropic.claude-haiku-4-5-20251001",
        "arn:aws:bedrock:eu-central-1::foundation-model/cohere.embed-english-v3",
        "arn:aws:bedrock:eu-central-1::foundation-model/cohere.rerank-v3"
      ]
    }
  ]
}
```

## Set environment

```bash
export AWS_REGION=eu-central-1
export BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-6-20251022
export BEDROCK_HAIKU_ID=anthropic.claude-haiku-4-5-20251001
```

## Verify

```bash
make install
make run
```

If the agent returns a structured evidence pack (even if the scaffold version), the setup is working. From here you can iterate against the real agent code as the build progresses.

## Cost notes

The local CLI runs against synthetic data and typically costs **under $0.10 per query** at Sonnet rates. The eval harness against the full 200-item golden set costs roughly **$2-4 per run** at the current Bedrock pricing. The eval-harness cost dominates a development month's bill; the per-query CLI use does not.

For tighter cost control, set `BEDROCK_MODEL_ID=anthropic.claude-haiku-4-5-20251001` to run the whole pipeline on Haiku — quality is materially lower for synthesis but adequate for exercising the plumbing.
