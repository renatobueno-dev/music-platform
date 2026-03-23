# Istio Traffic Management

Defines the external and internal request path through the Istio mesh.

## Traffic path

External client request path:

1. Client sends HTTP request to Istio ingress gateway.
2. Istio `Gateway` accepts host `playcatch.local` on port `80`.
3. Istio `VirtualService` routes traffic to `music-platform-api.music-platform.svc.cluster.local:8000`.
4. Kubernetes Service forwards to API pod (`api` container).

In-cluster request path:

1. Workload calls `music-platform-api.music-platform.svc.cluster.local:8000`.
2. Kubernetes Service load-balances to API pods.
3. Sidecar proxies (`istio-proxy`) enforce Istio traffic rules.

## Kubernetes vs Istio responsibilities

- Kubernetes `Service` (`ClusterIP`): stable internal endpoint and pod discovery.
- Istio `Gateway`: ingress entry point into the mesh.
- Istio `VirtualService`: HTTP host/path routing policy.
- Istio `DestinationRule`: destination traffic policy inside the mesh.

## Applied manifests

- `k8s/istio/traffic-management.yaml`
  - `Gateway/playcatch-gateway`
  - `VirtualService/playcatch-api-ingress`

Already present in namespace:

- `VirtualService/music-platform-api` (internal mesh route)
- `DestinationRule/music-platform-api`

## Quick validation

```bash
kubectl get gateway,virtualservice,destinationrule -n music-platform
kubectl port-forward -n istio-system svc/istio-ingressgateway 18080:80
curl -H "Host: playcatch.local" http://127.0.0.1:18080/health
```

Expected:

- Host `playcatch.local` returns API response.
- Requests without that host return `404` from ingress routing.
