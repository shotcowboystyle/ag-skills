---
name: k8s-security-policies
description: Implement Kubernetes security policies with Pod Security Admission, NetworkPolicy, RBAC and pod security contexts. Use when securing Kubernetes clusters, implementing network isolation, enforcing pod security standards, or migrating off PodSecurityPolicy.
last_verified: 2026-10-27
---

# Kubernetes Security Policies

Layered workload security with built-in Kubernetes APIs: Pod Security Admission
(PSA) for what pods may run, NetworkPolicy for who they may talk to, RBAC for
what identities may do, and security contexts on the pods themselves.

PodSecurityPolicy was removed in Kubernetes 1.25. Pod Security Admission, built
into the API server, replaces it. Do not write PSP manifests.

## Procedure

1. **Pick a Pod Security level per namespace.** `restricted` for application
   namespaces, `baseline` where a workload genuinely needs more, `privileged`
   only for system namespaces (CNI, storage, node agents).
2. **Dry-run it before enforcing.** The server reports every existing pod that
   would violate the level, without changing anything:

   ```bash
   kubectl label --dry-run=server --overwrite ns production \
     pod-security.kubernetes.io/enforce=restricted
   ```

3. **Label the namespace** (below). Start with `warn` and `audit` if pods still
   violate, then add `enforce`.
4. **Fix pod specs** with a restricted security context (below) until the
   dry-run is clean.
5. **Default-deny traffic**, then allow DNS and each required flow
   (`assets/network-policy-template.yaml`). Confirm the CNI enforces
   NetworkPolicy; some do not, and then policies are silently ignored.
6. **Give each workload its own ServiceAccount** with a namespaced Role that
   lists only the verbs and resources it uses (`references/rbac-patterns.md`).
7. **Verify** with `kubectl auth can-i` and a test pod (Troubleshooting).

## Pod Security Admission

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    # Pin the policy version so a cluster upgrade can't tighten it unannounced
    pod-security.kubernetes.io/enforce-version: v1.37
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
```

`warn` and `audit` at `latest` show what the next policy version will reject
before you move `enforce-version` forward.

## Restricted Pod Security Context

The minimum a pod needs to pass the `restricted` level:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
  namespace: production
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: registry.example.com/myapp:1.0.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true # not required by PSA, but recommended
        capabilities:
          drop: ["ALL"]
```

## Network Policies

```yaml
# Deny all ingress and egress for every pod in the namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes: ["Ingress", "Egress"]
---
# Allow DNS to the cluster DNS pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes: ["Egress"]
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

Select namespaces with the `kubernetes.io/metadata.name` label, which the API
server sets on every namespace. A hand-added `name:` label may not exist. More
flows (frontend to backend, ingress controller, monitoring, external HTTPS,
database) are in `assets/network-policy-template.yaml`.

## RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
automountServiceAccountToken: false # opt in per pod only if it calls the API
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["my-app-config"]
    verbs: ["get", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-app
  namespace: production
subjects:
  - kind: ServiceAccount
    name: my-app
    namespace: production
roleRef:
  kind: Role
  name: my-app
  apiGroup: rbac.authorization.k8s.io
```

Prefer Roles over ClusterRoles, name resources where you can, and avoid `*`.
`list` and `watch` on Secrets expose every Secret's contents, not only names.
More patterns: `references/rbac-patterns.md`.

## Beyond the built-ins

- **Custom admission rules** (required labels, allowed registries):
  ValidatingAdmissionPolicy (`admissionregistration.k8s.io/v1`, GA since 1.30)
  runs CEL in the API server with no extra component. Kyverno or OPA Gatekeeper
  add mutation, image verification and policy reports.
- **Service mesh mTLS and L7 authorization**: see the `mtls-configuration`
  skill in the `cloud-infrastructure` plugin.

## Troubleshooting

```bash
# Which pods in a namespace would a level reject?
kubectl label --dry-run=server --overwrite ns <ns> pod-security.kubernetes.io/enforce=restricted

# Pod rejected at admission: the event names the failing check
kubectl get events -n <ns> --field-selector reason=FailedCreate

# Effective permissions of a ServiceAccount
kubectl auth can-i --list --as system:serviceaccount:<ns>:<sa> -n <ns>

# NetworkPolicy has no effect: test from a pod the policy selects
kubectl run nettest -n <ns> --rm -it --image=busybox:1.37 --labels app=frontend -- \
  wget -qO- -T 3 http://backend:8080
```

## Related Skills

- `k8s-manifest-generator` - For creating secure manifests
- `gitops-workflow` - For automated policy deployment
