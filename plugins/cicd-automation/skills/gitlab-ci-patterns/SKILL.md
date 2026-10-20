---
name: gitlab-ci-patterns
description: Build GitLab CI/CD pipelines with multi-stage workflows, caching, and distributed runners for scalable automation. Use when implementing GitLab CI/CD, optimizing pipeline performance, or setting up automated testing and deployment.
last_verified: 2026-10-20
---

# GitLab CI Patterns

Pipeline patterns for building, testing, scanning and deploying with GitLab CI/CD.

## Rules that keep examples runnable

1. **Use `rules:`**, not `only:`/`except:` (deprecated, and they can't be mixed with `rules:`).
2. **Override tool-image entrypoints.** `hashicorp/terraform`, `aquasec/trivy` and
   similar images set `ENTRYPOINT` to the tool, so the runner's shell script fails. Add
   `entrypoint: [""]`.
3. **Keep `before_script` inside a template.** A top-level `before_script` runs in every
   job, including ones that use a different image.
4. **Secrets never reach the command line.** Use `--password-stdin`, masked and protected
   variables, and `id_tokens` (JWT) for Vault or cloud auth. Cluster access goes through
   the GitLab agent for Kubernetes, not a stored token.
5. **Scans that must block don't set `allow_failure: true`.**
6. Confirm with the user before adding jobs that deploy or run `terraform apply`.

## Basic pipeline

```yaml
stages: [build, test, deploy]

build:
  stage: build
  image: node:24
  script:
    - npm ci
    - npm run build
  cache:
    key: { files: [package-lock.json] }
    paths: [.npm/]
  variables:
    npm_config_cache: .npm
  artifacts:
    paths: [dist/]
    expire_in: 1 hour

test:
  stage: test
  image: node:24
  script:
    - npm ci
    - npm run lint
    - npm test
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

deploy:
  stage: deploy
  image:
    name: alpine/k8s:1.37.1 # bitnami/kubectl left the free catalog
    entrypoint: [""]
  script:
    - kubectl config use-context my-group/my-agent-project:production
    - kubectl apply -f k8s/
    - kubectl rollout status deployment/my-app --timeout=5m
  environment:
    name: production
    url: https://app.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

`kubectl config use-context <agent-project-path>:<agent-name>` works once a GitLab agent
for Kubernetes is installed in the cluster and authorizes this project. The runner gets
a short-lived kubeconfig; no cluster token is stored in CI variables.

## Docker build and push

```yaml
build-image:
  stage: build
  image: docker:29
  services: [docker:29-dind]
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - printf '%s' "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
  script:
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
```

## Multi-environment deployment

```yaml
.deploy:
  stage: deploy
  image:
    name: alpine/k8s:1.37.1
    entrypoint: [""]
  before_script:
    - kubectl config use-context "my-group/my-agent-project:$KUBE_AGENT"
  script:
    - kubectl apply -f k8s/ -n "$CI_ENVIRONMENT_NAME"
    - kubectl rollout status deployment/my-app -n "$CI_ENVIRONMENT_NAME" --timeout=5m

deploy:staging:
  extends: .deploy
  variables: { KUBE_AGENT: staging }
  environment: { name: staging, url: https://staging.example.com }
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy:production:
  extends: .deploy
  variables: { KUBE_AGENT: production }
  environment: { name: production, url: https://app.example.com }
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

Mark `production` as a protected environment so only allowed users can run the job.

## Terraform pipeline

```yaml
stages: [validate, plan, apply]

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform

.terraform:
  image:
    name: hashicorp/terraform:1.16
    entrypoint: [""]
  before_script:
    - cd "$TF_ROOT"
    - terraform init -input=false

validate:
  extends: .terraform
  stage: validate
  before_script:
    - cd "$TF_ROOT"
    - terraform init -backend=false -input=false
  script:
    - terraform fmt -check
    - terraform validate

plan:
  extends: .terraform
  stage: plan
  script:
    - terraform plan -input=false -out=tfplan
  artifacts:
    paths: [terraform/tfplan]
    access: developer # the plan file can hold sensitive values
    expire_in: 1 day

apply:
  extends: .terraform
  stage: apply
  needs: [plan]
  script:
    - terraform apply -input=false tfplan
  environment: { name: production }
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

## Security scanning (blocking)

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Dependency-Scanning.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml

trivy-image:
  stage: test
  needs: [build-image]
  image:
    name: aquasec/trivy:0.76.0
    entrypoint: [""]
  variables:
    TRIVY_USERNAME: $CI_REGISTRY_USER
    TRIVY_PASSWORD: $CI_REGISTRY_PASSWORD
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
```

`--exit-code 1` fails the job on a finding; adding `allow_failure: true` would turn that
back into a warning. For TruffleHog, see `secrets-management`.

## Caching

```yaml
build:
  cache:
    - key: { files: [package-lock.json] } # changes only when deps change
      paths: [.npm/]
      policy: pull-push

lint:
  cache:
    - key: { files: [package-lock.json] }
      paths: [.npm/]
      policy: pull # read-only; don't re-upload
```

## Dynamic child pipelines

```yaml
generate-pipeline:
  stage: build
  script:
    - python generate_pipeline.py > child-pipeline.yml
  artifacts:
    paths: [child-pipeline.yml]

trigger-child:
  stage: deploy
  trigger:
    include:
      - artifact: child-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

## Related Skills

- `github-actions-templates` - For GitHub Actions
- `deployment-pipeline-design` - For architecture
- `secrets-management` - For secrets handling
