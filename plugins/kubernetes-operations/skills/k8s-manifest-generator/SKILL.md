---
name: k8s-manifest-generator
description: Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations.
last_verified: 2026-10-27
---

# Kubernetes Manifest Generator

Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims.

## Purpose

This skill provides comprehensive guidance for generating well-structured, secure, and production-ready Kubernetes manifests following cloud-native best practices and Kubernetes conventions.

## When to Use This Skill

Use this skill when you need to:

- Create new Kubernetes Deployment manifests
- Define Service resources for network connectivity
- Generate ConfigMap and Secret resources for configuration management
- Create PersistentVolumeClaim manifests for stateful workloads
- Follow Kubernetes best practices and naming conventions
- Implement resource limits, health checks, and security contexts
- Design manifests for multi-environment deployments

## Procedure

1. **Gather requirements**: workload type (stateless, stateful, batch), image
   and an immutable tag or digest, ports, config and secrets, storage, CPU and
   memory, replica count, health endpoints, and whether it is exposed outside
   the cluster. Ask for anything missing rather than inventing it.
2. **Pick the workload kind**: Deployment for stateless services, StatefulSet
   for stable identity or per-replica storage, Job or CronJob for batch.
3. **Write the workload** from `assets/deployment-template.yaml`. Every
   container gets resource requests (and a memory limit), readiness and
   liveness probes, and a restricted security context: `runAsNonRoot: true`,
   `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`,
   `seccompProfile.type: RuntimeDefault`. That is what a namespace at the
   `restricted` Pod Security level admits.
4. **Expose it** with a Service from `assets/service-template.yaml`: ClusterIP
   by default, LoadBalancer only for direct external access. The Service
   selector must match the pod template labels exactly.
5. **Externalise configuration**: ConfigMaps from
   `assets/configmap-template.yaml`; Secrets never committed in plain text (use
   External Secrets, Sealed Secrets or SOPS).
6. **Add storage** if needed: a PersistentVolumeClaim with an explicit
   `storageClassName` and access mode.
7. **Label consistently** with the `app.kubernetes.io/*` recommended labels
   (`name`, `instance`, `version`, `component`, `part-of`, `managed-by`).
8. **Validate offline** against the target Kubernetes version, then
   server-side when a cluster is available:

   ```bash
   kubeconform -strict -summary -kubernetes-version 1.37.0 manifests/
   kubectl apply --dry-run=server -f manifests/
   ```

   kubeconform replaces kubeval, which is unmaintained and has no schemas for
   current Kubernetes. CRDs need extra `-schema-location` entries (see
   `references/details.md`, step 10).

## References

- `references/details.md`: the full step-by-step workflow with worked examples,
  multi-resource layout and common patterns
- `references/deployment-spec.md`: every Deployment field worth setting
- `references/service-spec.md`: Service types, traffic policies, headless
  Services and external endpoints

## Best Practices Summary

1. **Always set resource requests and limits** - Prevents resource starvation
2. **Implement health checks** - Ensures Kubernetes can manage your application
3. **Use specific image tags** - Avoid unpredictable deployments
4. **Apply security contexts** - Run as non-root, drop capabilities
5. **Use ConfigMaps and Secrets** - Separate config from code
6. **Label everything** - Enables filtering and organization
7. **Follow naming conventions** - Use standard Kubernetes labels
8. **Validate before applying** - `kubeconform -strict`, then server-side dry-run
9. **Version your manifests** - Keep in Git with version control
10. **Document with annotations** - Add context for other developers

## Troubleshooting

**Pods not starting:**

- Check image pull errors: `kubectl describe pod <pod-name>`
- Verify resource availability: `kubectl get nodes`
- Check events: `kubectl get events --sort-by='.lastTimestamp'`

**Service not accessible:**

- Verify selector matches pod labels: `kubectl get endpointslices -l kubernetes.io/service-name=<service-name>` (no ready endpoints means no matching ready pods)
- Check service type and port configuration
- Test from within cluster: `kubectl run debug --rm -it --image=busybox:1.37 -- sh`

**ConfigMap/Secret not loading:**

- Verify names match in Deployment
- Check namespace
- Ensure resources exist: `kubectl get configmap,secret`

## Next Steps

After creating manifests:

1. Store in Git repository
2. Set up CI/CD pipeline for deployment
3. Consider using Helm or Kustomize for templating
4. Implement GitOps with ArgoCD or Flux
5. Add monitoring and observability

## Related Skills

- `helm-chart-scaffolding` - For templating and packaging
- `gitops-workflow` - For automated deployments
- `k8s-security-policies` - For advanced security configurations
