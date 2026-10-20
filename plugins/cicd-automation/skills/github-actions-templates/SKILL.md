---
name: github-actions-templates
description: Create production-ready GitHub Actions workflows for automated testing, building, and deploying applications. Use when setting up CI/CD with GitHub Actions, automating development workflows, or creating reusable workflow templates.
last_verified: 2026-10-20
---

# GitHub Actions Templates

Workflow patterns for testing, building, scanning and deploying.

## Baseline for every workflow

1. **`permissions: contents: read` at the top**, then grant more per job.
2. **Pin actions to a full commit SHA** with the version in a comment. Tags can be moved:
   in March 2026 an attacker force-pushed 76 `trivy-action` tags to malware
   (GHSA-69fq-xp46-6x23). Let Dependabot or Renovate bump the SHAs.
3. **Cloud auth uses OIDC** (`id-token: write` + a role), never stored access keys.
4. **Production deploys run in an `environment:`** with required reviewers and branch rules.
5. **Supported runtimes only**: Node 22/24, Python 3.12+. Check
   [endoflife.date](https://endoflife.date) before adding a version.
6. Confirm with the user before adding a workflow that deploys or pushes.

Resolve a SHA: `gh api repos/OWNER/REPO/commits/TAG --jq .sha`.

## Test

```yaml
name: Test
on:
  push: { branches: [main] }
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write # Codecov OIDC upload, no token secret
    strategy:
      matrix:
        node-version: [22, 24]
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - uses: codecov/codecov-action@303a32d7a59b442fa8d48b6a1cc6825c09c847a5 # v7.1.1
        with:
          files: ./coverage/lcov.info
          use_oidc: true
```

Python matrix: `python-version: ["3.12", "3.13", "3.14"]` with
`actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`.

## Build and push an image

```yaml
name: Build
on:
  push:
    branches: [main]
    tags: ["v*"]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: docker/setup-buildx-action@f87e5991a6d7451dcb8d9637bfbc97413f497069 # v4.4.1
      - uses: docker/login-action@dbcb813823bdd20940b903addbd779551569679f # v4.6.0
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@dc802804100637a589fabce1cb79ff13a1411302 # v6.2.0
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha
      - uses: docker/build-push-action@c3c9e263c25d99ce0380d002d59b67737d91b0dc # v7.4.0
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Deploy to EKS (OIDC + environment)

```yaml
name: Deploy
on:
  push: { branches: [main] }

permissions:
  contents: read

concurrency: { group: deploy-production, cancel-in-progress: false }

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production # required reviewers + allowed branches set in repo settings
      url: https://app.example.com
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-deploy-prod
          aws-region: us-west-2
      - run: aws eks update-kubeconfig --name production-cluster --region us-west-2
      - run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/my-app -n production --timeout=5m
```

Pin the role's trust policy `sub` to `repo:my-org/my-repo:environment:production`, so
only this environment can assume it.

## Reusable workflow

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version: { required: true, type: string }

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
        with: { node-version: "${{ inputs.node-version }}" }
      - run: npm ci && npm test
```

Caller: `uses: ./.github/workflows/reusable-test.yml` with `with: { node-version: "24" }`.
Pass secrets by name, not `secrets: inherit`.

## Security scanning (blocking)

```yaml
name: Security
on:
  push: { branches: [main] }
  pull_request:

permissions:
  contents: read

jobs:
  trivy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25 # v0.36.0
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: "1" # fail the job on a finding
          format: sarif
          output: trivy.sarif
      - if: always() # upload even when the scan failed
        uses: github/codeql-action/upload-sarif@6f2ac81f5cd81fe351a197ba0b00d91d03cd2aee # v4.39.0
        with: { sarif_file: trivy.sarif }
```

`snyk/actions/node@9adf32b1121593767fc3c057af55b55db032dc04 # v1.0.0` fails on any
vulnerability by default (`args: --severity-threshold=high` to narrow). Secret scanning
is in `secrets-management`.

## Notify after deploy

```yaml
- if: success()
  uses: slackapi/slack-github-action@dcb1066f776dd043e64d0e8ba94ca15cc7e1875d # v4.0.0
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK_URL }}
    webhook-type: incoming-webhook
    payload: |
      text: "Deployed ${{ github.sha }} to production"
```

## Related Skills

- `gitlab-ci-patterns` - For GitLab CI workflows
- `deployment-pipeline-design` - For pipeline architecture
- `secrets-management` - For secrets handling
