---
name: helm-chart-scaffolding
description: Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments.
last_verified: 2026-10-27
---

# Helm Chart Scaffolding

Comprehensive guidance for creating, organizing, and managing Helm charts for packaging and deploying Kubernetes applications.

## Purpose

This skill provides step-by-step instructions for building production-ready Helm charts, including chart structure, templating patterns, values management, and validation strategies.

## When to Use This Skill

Use this skill when you need to:

- Create new Helm charts from scratch
- Package Kubernetes applications for distribution
- Manage multi-environment deployments with Helm
- Implement templating for reusable Kubernetes manifests
- Set up Helm chart repositories
- Follow Helm best practices and conventions

## Procedure

1. **Scaffold**: `helm create my-app`, then delete the templates the app does
   not need. Fill `Chart.yaml` from `assets/Chart.yaml.template` with
   `apiVersion: v2`, a SemVer `version` (the chart) and `appVersion` (the image).
2. **Design `values.yaml`** from `assets/values.yaml.template`: every value
   commented, safe defaults (non-root security context, resource requests,
   probes), and a pinned image tag. Add `values.schema.json` so bad values fail
   at install time instead of rendering broken manifests.
3. **Template**: put names, labels and selectors in `_helpers.tpl` and include
   them everywhere; gate optional resources (Ingress, HPA) behind `enabled`
   flags; quote strings and use `required` for values with no safe default.
4. **Pin dependencies** in `Chart.yaml` with exact or tightly bounded versions,
   then `helm dependency update` and commit `Chart.lock`.
5. **Validate offline**, with no cluster needed:

   ```bash
   helm lint ./my-app
   helm template my-app ./my-app | kubeconform -strict -summary -kubernetes-version 1.37.0
   helm template my-app ./my-app -f values-prod.yaml | kubeconform -strict -summary -kubernetes-version 1.37.0
   ```

   or run `scripts/validate-chart.sh ./my-app`, which also checks structure,
   security context, resources and probes.
6. **Validate against a cluster** when one is available:
   `helm install my-app ./my-app --dry-run=server`. On Helm 3, every
   `helm install --dry-run` contacts the cluster, so use `helm template` for
   offline checks.
7. **Package and publish**: `helm package`, then `helm push` to an OCI registry.

## References

- `references/details.md`: full workflow with worked examples, multi-environment
  values, hooks and tests, common template patterns
- `references/chart-structure.md`: directory layout, `Chart.yaml` fields,
  dependencies, CRDs, versioning

## Best Practices

1. **Use semantic versioning** for chart and app versions
2. **Document all values** in values.yaml with comments
3. **Use template helpers** for repeated logic
4. **Validate charts** before packaging
5. **Pin dependency versions** explicitly
6. **Use conditions** for optional resources
7. **Follow naming conventions** (lowercase, hyphens)
8. **Include NOTES.txt** with usage instructions
9. **Add labels** consistently using helpers
10. **Test installations** in all environments

## Troubleshooting

**Template rendering errors:**

```bash
helm template my-app ./my-app --debug
```

**Dependency issues:**

```bash
helm dependency update
helm dependency list
```

**Installation failures:**

```bash
helm install my-app ./my-app --dry-run=server --debug
kubectl get events --sort-by='.lastTimestamp'
```


## Related Skills

- `k8s-manifest-generator` - For creating base Kubernetes manifests
- `gitops-workflow` - For automated Helm chart deployments
