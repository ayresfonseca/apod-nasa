---
description: "Use when creating or modifying Kubernetes manifests in deploy/. Covers deployment structure, nginx sidecar pattern, probe endpoints, image references, Kustomize, and HTTPRoute vs Ingress conventions for this project."
applyTo: "deploy/*.yml"
---

# Kubernetes Deploy Manifests — apod-nasa

## Architecture: nginx + Flask sidecar

All traffic enters through the **nginx sidecar** on port 80; it proxies to Flask/uWSGI on `127.0.0.1:8000` (same Pod, loopback only). Never expose Flask directly via the Service.

```
Service:80 → nginx container:80 → proxy → flask-app container:8000
```

## Probe endpoints

| Container   | Liveness                       | Readiness                      |
|-------------|--------------------------------|--------------------------------|
| `nginx`     | `GET /healthz :80`             | `GET /healthz :80`             |
| `flask-app` | `GET /flask-healthz :8000`     | `GET /healthz :80` (via nginx) |

- `/healthz` is served by nginx directly (static 200); it does **not** proxy to Flask.
- `/flask-healthz` is the Flask app's own health route.

## Image references

- **nginx**: use `nginx:stable` (not `nginx:latest`)
- **flask-app**: use a pinned tag `ghcr.io/ayresfonseca/apod-nasa:<version>` in production; `latest` is only acceptable as a placeholder before tagging a release
- Pull secret `ghcr-apod` must be present in the target namespace; always include `imagePullSecrets`

## Resource budgets (baseline)

Both containers share the same baseline; adjust only if load testing justifies it:

```yaml
resources:
  requests:
    memory: 64Mi
    cpu: 25m
  limits:
    memory: 128Mi
    cpu: 50m
```

## ConfigMap — nginx config

`default.conf` is **not** committed as a raw ConfigMap manifest. Kustomize generates it via `configMapGenerator` in `kustomization.yml`:

```yaml
configMapGenerator:
  - name: nginx-default-conf
    files:
      - default.conf
```

Edit `deploy/default.conf` to change nginx config; never inline it in `deployment.yml`.

## HTTPRoute vs Ingress

Two routing resources coexist deliberately:

| File             | Controller                    | Status          |
|------------------|-------------------------------|-----------------|
| `httproute.yml`  | Envoy Gateway (Gateway API)   | Active/primary  |
| `ingress.yml`    | Traefik                       | Legacy, kept for fallback |

- `httproute.yml` uses `parentRefs` pointing to `eg-private` in namespace `envoy-gateway-system`
- `ingress.yml` uses `cert-manager.io/cluster-issuer: letsencrypt-prod` annotation for TLS
- Hostname in both: `apod.anetwork.cloud`
- Do not remove `ingress.yml` without confirming Traefik is no longer in use

## Apply

```sh
kubectl apply -k deploy/    # always apply via Kustomize, not kubectl apply -f
```
