# linkerd-patterns — routing, authorization and multi-cluster

## HTTPRoute for Advanced Routing

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-route
  namespace: my-namespace
spec:
  parentRefs:
    - name: my-service
      kind: Service
      group: ""
      port: 8080
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/v2
        - headers:
            - name: x-api-version
              value: v2
      backendRefs:
        - name: my-service-v2
          port: 8080
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: my-service-v1
          port: 8080
```

## Authorization Policy

```yaml
# Name the port to protect
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: my-service-http
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      app: my-service
  port: http
  proxyProtocol: HTTP/1
---
# Who may call it: the frontend's mesh identity
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata:
  name: frontend
  namespace: my-namespace
spec:
  identityRefs:
    - kind: ServiceAccount
      name: frontend
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: my-namespace
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: my-service-http
  requiredAuthenticationRefs:
    - group: policy.linkerd.io
      kind: MeshTLSAuthentication
      name: frontend
---
# Unauthenticated traffic from a network (for example an unmeshed ingress)
apiVersion: policy.linkerd.io/v1alpha1
kind: NetworkAuthentication
metadata:
  name: ingress-network
  namespace: my-namespace
spec:
  networks:
    - cidr: 10.0.0.0/8
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: allow-ingress
  namespace: my-namespace
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: my-service-http
  requiredAuthenticationRefs:
    - group: policy.linkerd.io
      kind: NetworkAuthentication
      name: ingress-network
```

Once a Server exists, traffic to that port is denied unless a policy allows it,
so create the policies before or together with the Server.

## Multi-cluster Setup

Both clusters need a shared trust anchor. Then, to let `west` reach services
in `east`:

```bash
# Install the multicluster extension on both clusters
for ctx in west east; do
  linkerd --context=$ctx multicluster install | kubectl --context=$ctx apply -f -
done

# Generate the Link (and its credentials) from the target cluster,
# apply it to the source cluster
linkerd --context=east multicluster link-gen --cluster-name east \
  | kubectl --context=west apply -f -

# Export a service from east
kubectl --context=east label svc/my-service mirror.linkerd.io/exported=true

# Verify cross-cluster connectivity from west
linkerd --context=west multicluster check
linkerd --context=west multicluster gateways
```

`linkerd multicluster link` is deprecated in favour of `link-gen`. Recent
releases manage service-mirror controllers from the extension's values
(`controllers:`); see the multicluster task in the Linkerd docs.
