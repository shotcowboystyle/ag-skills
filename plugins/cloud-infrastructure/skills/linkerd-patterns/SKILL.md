---
name: linkerd-patterns
description: Implement Linkerd service mesh patterns for lightweight, security-focused service mesh deployments. Use when setting up Linkerd, configuring traffic policies, or implementing zero-trust networking with minimal overhead.
last_verified: 2026-10-27
---

# Linkerd Patterns

Production patterns for Linkerd service mesh - the lightweight, security-first service mesh for Kubernetes.

## When to Use This Skill

- Setting up a lightweight service mesh
- Implementing automatic mTLS
- Configuring weighted traffic splits for canary deployments
- Per-route routing, retries and timeouts with Gateway API routes
- Multi-cluster service mesh

## Core Concepts

### 1. Linkerd Architecture

```
┌─────────────────────────────────────────────┐
│                Control Plane                │
│ ┌───────────┐ ┌──────────┐ ┌────────────┐   │
│ │destination│ │ identity │ │proxy-inject│   │
│ └───────────┘ └──────────┘ └────────────┘   │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────┐
│                 Data Plane                   │
│  ┌─────┐    ┌─────┐    ┌─────┐             │
│  │proxy│────│proxy│────│proxy│             │
│  └─────┘    └─────┘    └─────┘             │
│     │           │           │               │
│  ┌──┴──┐    ┌──┴──┐    ┌──┴──┐            │
│  │ app │    │ app │    │ app │            │
│  └─────┘    └─────┘    └─────┘            │
└─────────────────────────────────────────────┘
```

### 2. Key Resources

| Resource                                     | Purpose                                                 |
| -------------------------------------------- | ------------------------------------------------------- |
| **HTTPRoute / GRPCRoute** (Gateway API)      | Routing, weighted splits, retries and timeouts per route |
| **Server**                                   | Names a port on a set of pods for policy                |
| **AuthorizationPolicy**                      | Allows traffic to a Server, route or namespace          |
| **MeshTLSAuthentication / NetworkAuthentication** | Who the policy allows: mesh identities or CIDRs     |

Linkerd's routing and policy features use the Kubernetes Gateway API types. SMI
`TrafficSplit` (the SMI project is archived) and the `linkerd-smi` extension are
not used for new setups. ServiceProfiles still work, but new features land on
HTTPRoute/GRPCRoute, and a ServiceProfile on a Service overrides any route-level
retry and timeout annotations.

## Templates

### Template 1: Mesh Installation

The Linkerd project publishes open-source *edge* releases (`edge-YY.M.N`);
versioned stable releases come from vendors. Use a CLI version that matches the
control plane. The example uses Homebrew; for other systems, follow the
[official installation guide](https://linkerd.io/2-edge/getting-started/).

```bash
# Install the CLI with Homebrew
brew install linkerd
linkerd version

# Linkerd needs the Gateway API CRDs. Check whether they are already installed
# (prints the bundle version) and that it is in Linkerd's compatibility table
kubectl get crds/httproutes.gateway.networking.k8s.io \
  -o "jsonpath={.metadata.annotations.gateway\.networking\.k8s\.io/bundle-version}"
# If not found, install a compatible version (1.5.1 at the time of writing)
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.5.1/standard-install.yaml

# Validate cluster
linkerd check --pre

# Install CRDs
linkerd install --crds | kubectl apply -f -

# Install control plane
linkerd install | kubectl apply -f -

# Verify installation
linkerd check

# Install viz extension (optional)
linkerd viz install | kubectl apply -f -
```

### Template 2: Inject Namespace

```yaml
# Automatic injection for namespace
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
  annotations:
    linkerd.io/inject: enabled
---
# Or inject specific deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
      annotations:
        linkerd.io/inject: enabled # on the pod template, not the Deployment
    spec:
      containers:
        - name: app
          image: registry.example.com/my-app:1.0.0
```

### Template 3: Retries and Timeouts on a Route

Retries are opt-in and only safe for idempotent requests, so put them on a
route that matches only those requests.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: users-get
  namespace: my-namespace
  annotations:
    retry.linkerd.io/http: 5xx
    retry.linkerd.io/limit: "2"
    retry.linkerd.io/timeout: 300ms # per-attempt timeout
    timeout.linkerd.io/request: 5s # whole request, including retries
spec:
  parentRefs:
    - name: my-service
      kind: Service
      group: ""
      port: 8080
  rules:
    - matches:
        - method: GET
          path:
            type: PathPrefix
            value: /api/users
      backendRefs:
        - name: my-service
          port: 8080
```

The same annotations on the Service apply to every route of that Service.

### Template 4: Weighted Traffic Split (Canary)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-service-canary
  namespace: my-namespace
spec:
  parentRefs:
    - name: my-service
      kind: Service
      group: ""
      port: 8080
  rules:
    - backendRefs:
        - name: my-service-stable
          port: 8080
          weight: 90
        - name: my-service-canary
          port: 8080
          weight: 10
```

Shift the weights step by step, or let Flagger or Argo Rollouts (Gateway API
plugin) drive them.

### More templates

`references/details.md` covers header- and path-based routing with HTTPRoute,
authorization policy (Server, AuthorizationPolicy, MeshTLSAuthentication,
NetworkAuthentication) and multi-cluster linking with `link-gen`.

## Monitoring Commands

```bash
# Live traffic view
linkerd viz top deploy/my-app

# Per-route metrics (HTTPRoute/GRPCRoute or ServiceProfile routes)
linkerd viz routes deploy/my-app

# Check proxy status
linkerd viz stat deploy -n my-namespace

# View service dependencies
linkerd viz edges deploy -n my-namespace

# Dashboard
linkerd viz dashboard
```

## Debugging

```bash
# Check injection status
linkerd check --proxy -n my-namespace

# View proxy logs
kubectl logs deploy/my-app -c linkerd-proxy

# Debug identity/TLS
linkerd identity -n my-namespace

# Tap traffic (live)
linkerd viz tap deploy/my-app --to deploy/my-backend
```

## Best Practices

### Do's

- **Enable mTLS everywhere** - It's automatic with Linkerd
- **Use HTTPRoute/GRPCRoute** - Per-route routing, retries and timeouts
- **Limit retries** - Retry idempotent routes only, with `retry.linkerd.io/limit`
- **Monitor golden metrics** - Success rate, latency, throughput

### Don'ts

- **Don't skip check** - Always run `linkerd check` after changes
- **Don't over-configure** - Linkerd defaults are sensible
- **Don't mix ServiceProfiles and route annotations** - A ServiceProfile overrides route-level retries and timeouts
- **Don't forget timeouts** - Set appropriate values per route
