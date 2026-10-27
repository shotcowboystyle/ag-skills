# ArgoCD Setup and Configuration

## Installation Methods

Pin a release tag rather than `stable`, and apply server-side: some Argo CD CRDs
exceed the annotation size limit of client-side `kubectl apply`. Versions below
were current on 2026-10-27; check the
[releases](https://github.com/argoproj/argo-cd/releases) page.

### 1. Standard Installation

```bash
ARGOCD_VERSION=v3.5.6
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml"
```

### 2. High Availability Installation

Needs at least three nodes for the pod anti-affinity rules.

```bash
kubectl apply -n argocd --server-side --force-conflicts \
  -f "https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/ha/install.yaml"
```

### 3. Helm Installation

The chart has its own version line; chart 10.11.6 ships Argo CD v3.5.6
(`helm search repo argo/argo-cd --versions` lists the mapping).

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd --version 10.11.6 -n argocd --create-namespace
```

## Initial Configuration

### Access ArgoCD UI

```bash
# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
argocd admin initial-password -n argocd
```

### Rotate the Admin Password

The initial password is stored in plain text in `argocd-initial-admin-secret`.
Change it, then delete the secret (Argo CD only recreates it if a new admin
password has to be generated):

```bash
argocd login localhost:8080 --username admin
argocd account update-password
kubectl -n argocd delete secret argocd-initial-admin-secret
```

After SSO is configured, disable the local admin user with
`admin.enabled: "false"` in `argocd-cm`.

### Expose with Gateway API

ingress-nginx was retired in March 2026, so expose the API server through a
Gateway API implementation. This example terminates TLS at an existing
`Gateway` (`cluster-gateway` in namespace `gateway`, with an HTTPS listener named
`https`) and runs `argocd-server` without its own TLS. Set
`server.insecure: "true"` in the `argocd-cmd-params-cm` ConfigMap and restart
`argocd-server`, or keep TLS to the backend with a `BackendTLSPolicy`.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: argocd-http
  namespace: argocd
spec:
  parentRefs:
    - name: cluster-gateway
      namespace: gateway
      sectionName: https
  hostnames:
    - argocd.example.com
  rules:
    - backendRefs:
        - name: argocd-server
          port: 80
---
# The argocd CLI works best over gRPC; give it its own hostname
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: argocd-grpc
  namespace: argocd
spec:
  parentRefs:
    - name: cluster-gateway
      namespace: gateway
      sectionName: https
  hostnames:
    - grpc.argocd.example.com
  rules:
    - backendRefs:
        - name: argocd-server
          port: 443
```

For the gRPC route, mark the `argocd-server` Service's `https` port as HTTP/2
with `appProtocol: kubernetes.io/h2c` (Helm value
`server.service.servicePortHttpsAppProtocol`).

For other setups (TLS passthrough, other ingress controllers), see the Argo CD
[ingress guide](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/).

## CLI Configuration

### Login

```bash
argocd login argocd.example.com --username admin
```

### Add Repository

```bash
argocd repo add https://github.com/org/repo --username user --password token
```

### Create Application

```bash
argocd app create my-app \
  --repo https://github.com/org/repo \
  --path apps/my-app \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production
```

## SSO Configuration

### GitHub OAuth

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  url: https://argocd.example.com
  dex.config: |
    connectors:
      - type: github
        id: github
        name: GitHub
        config:
          clientID: <github-oauth-client-id>
          # Resolved from the dex.github.clientSecret key in the argocd-secret Secret
          clientSecret: $dex.github.clientSecret
          orgs:
          - name: my-org
```

## RBAC Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    p, role:developers, applications, *, */dev, allow
    p, role:operators, applications, *, */*, allow
    g, my-org:devs, role:developers
    g, my-org:ops, role:operators
```

## Best Practices

1. Enable SSO for production
2. Implement RBAC policies
3. Use separate projects for teams
4. Enable audit logging
5. Configure notifications
6. Use ApplicationSets for multi-cluster
7. Implement resource hooks
8. Configure health checks
9. Use sync windows for maintenance
10. Monitor with Prometheus metrics
