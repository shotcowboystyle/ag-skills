---
name: secrets-management
description: Implement secure secrets management for CI/CD pipelines using Vault, AWS Secrets Manager, or native platform solutions. Use when handling sensitive credentials, rotating secrets, or securing CI/CD environments.
last_verified: 2026-10-20
---

# Secrets Management

Keep secrets out of Git, out of logs and out of long-lived CI credentials.

## Rules

1. **CI authenticates with OIDC/JWT**, never a stored Vault token or AWS access key.
   The runner gets a short-lived identity token; the secret store trusts the issuer.
2. **Never print a secret.** No `echo $SECRET`, no `set -x` around secret use. Pass it
   to the process that needs it through the environment of that one step.
3. **Scanners must block.** A scan that exits 0 on a finding is decoration.
4. **Keep secrets out of IaC state.** Let the provider manage the value, or use
   write-only arguments.
5. **Scope per environment** and rotate. Confirm with the user before changing a
   production secret, Vault policy or IAM trust policy.

## HashiCorp Vault

### Trust GitHub Actions OIDC

```bash
vault auth enable jwt
vault write auth/jwt/config \
  oidc_discovery_url="https://token.actions.githubusercontent.com" \
  bound_issuer="https://token.actions.githubusercontent.com"

vault write auth/jwt/role/deploy-prod - <<'EOF'
{
  "role_type": "jwt",
  "user_claim": "repository",
  "bound_audiences": ["https://github.com/my-org"],
  "bound_claims": { "repository": "my-org/my-repo", "environment": "production" },
  "token_policies": ["deploy-prod"],
  "token_ttl": "10m"
}
EOF
```

For GitLab, use a second mount with `oidc_discovery_url="https://gitlab.com"` and bind
`project_path` and `ref_protected: "true"`.

### GitHub Actions

```yaml
permissions:
  contents: read
  id-token: write # mint the OIDC token

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: hashicorp/vault-action@892a26828f195e65540a40b4768ae4571f51ebfc # v4.0.0
        with:
          url: https://vault.example.com
          method: jwt
          role: deploy-prod
          jwtGithubAudience: https://github.com/my-org
          secrets: |
            secret/data/database password | DB_PASSWORD ;
            secret/data/api key | API_KEY
      - run: ./deploy.sh # reads $DB_PASSWORD and $API_KEY; the action masks them
```

### GitLab CI

```yaml
deploy:
  image:
    name: hashicorp/vault:2.2
    entrypoint: [""] # the image entrypoint runs `vault`, not the job script
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  variables:
    VAULT_ADDR: https://vault.example.com
  script:
    - export VAULT_TOKEN="$(vault write -field=token auth/jwt/login role=deploy-prod jwt="$VAULT_ID_TOKEN")"
    - export DB_PASSWORD="$(vault kv get -mount=secret -field=password database/config)"
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

GitLab Premium can replace the script with the `secrets:` keyword plus `id_tokens`.

## AWS Secrets Manager

### Store a secret

```bash
# From a file, so the value never lands in shell history
aws secretsmanager create-secret --name production/api-key \
  --secret-string file://api-key.json
```

### GitHub Actions (OIDC role)

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
    with:
      role-to-assume: arn:aws:iam::123456789012:role/gha-deploy-prod
      aws-region: us-west-2
  - name: Deploy
    run: |
      API_KEY="$(aws secretsmanager get-secret-value --secret-id production/api-key \
        --query SecretString --output text)" ./deploy.sh
```

The IAM role's trust policy must pin `token.actions.githubusercontent.com:sub` to the
repo and environment (`repo:my-org/my-repo:environment:production`).

### Terraform: keep the password out of state

```hcl
resource "aws_db_instance" "main" {
  allocated_storage           = 100
  engine                      = "postgres"
  instance_class              = "db.t3.large"
  username                    = "app_admin"
  manage_master_user_password = true # RDS creates, stores and rotates it in Secrets Manager
}
```

Reading `aws_secretsmanager_secret_version` into a resource argument writes the plaintext
to state. For resources without a managed option, use a write-only argument such as
`password_wo` (Terraform 1.11+).

## Rotation

Prefer managed rotation (RDS, Redshift, DocumentDB). A custom rotation Lambda must
implement all four steps; Secrets Manager calls it once per step with the same token.

```python
import boto3

sm = boto3.client("secretsmanager")

def lambda_handler(event, context):
    arn, token, step = event["SecretId"], event["ClientRequestToken"], event["Step"]
    if step == "createSecret":
        try:
            sm.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
        except sm.exceptions.ResourceNotFoundException:
            new = sm.get_random_password(PasswordLength=32, ExcludePunctuation=True)
            sm.put_secret_value(SecretId=arn, ClientRequestToken=token,
                                SecretString=new["RandomPassword"],
                                VersionStages=["AWSPENDING"])
    elif step == "setSecret":
        set_password_in_target(arn, token)   # apply AWSPENDING to the database/API
    elif step == "testSecret":
        test_login_with_pending(arn, token)  # raise on failure; rotation stops
    elif step == "finishSecret":
        meta = sm.describe_secret(SecretId=arn)
        current = next(v for v, s in meta["VersionIdsToStages"].items() if "AWSCURRENT" in s)
        if current != token:
            sm.update_secret_version_stage(SecretId=arn, VersionStage="AWSCURRENT",
                                           MoveToVersionId=token,
                                           RemoveFromVersionId=current)
    else:
        raise ValueError(f"unknown step {step}")
```

## Kubernetes: External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: https://vault.example.com
      path: secret
      version: v2
      auth:
        kubernetes:
          mountPath: kubernetes
          role: production
---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef: { name: vault-backend, kind: SecretStore }
  target: { name: database-credentials }
  data:
    - secretKey: password
      remoteRef: { key: database/config, property: password }
```

`v1beta1` is deprecated; use `external-secrets.io/v1`.

## Secret scanning

TruffleHog exits 0 on findings unless you pass `--fail` (then it exits 183).

### Pre-commit hook

```sh
#!/bin/sh
# .git/hooks/pre-commit: scans staged changes; a non-zero exit blocks the commit
exec docker run --rm -i -v "$(pwd):/workdir" trufflesecurity/trufflehog:3.99.3 \
  git file:///workdir --since-commit HEAD --results=verified,unknown --fail
```

### CI

```yaml
# GitLab
secret-scan:
  stage: test
  image:
    name: trufflesecurity/trufflehog:3.99.3
    entrypoint: [""]
  variables:
    GIT_DEPTH: 0
  script:
    - trufflehog git "file://$CI_PROJECT_DIR" --results=verified,unknown --fail
```

```yaml
# GitHub Actions
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  with: { fetch-depth: 0 }
- uses: trufflesecurity/trufflehog@e63326d6545de8f425d93ce24078c6e68d83f70e # v3.99.3
  with: { extra_args: --results=verified,unknown } # the action adds --fail
```

## Related Skills

- `github-actions-templates` - For GitHub Actions integration
- `gitlab-ci-patterns` - For GitLab CI integration
- `deployment-pipeline-design` - For pipeline architecture
