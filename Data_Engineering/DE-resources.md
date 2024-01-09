
# Create volume

```
mkdir -p /server/k3d
chmod 777 /server/k3d
```


# Create cluster

```
k3d cluster create minio --servers 3 --agents 3 -v /server/k3d:/var/lib/rancher/k3s/storage@all --k3s-arg "--tls-san=61.101.244@server:*" --k3s-arg "--disable=traefik@server:*" --k3s-arg "--service-node-port-range=30000-30050@server:*" -p "30050:30050@loadbalancer:*" -p "80:80@loadbalancer:*" -p "443:443@loadbalancer:*" --timeout 10m

k3d cluster create onion-dev --servers 1 --agents 2 -v /home/jose/server/k3d:/var/lib/rancher/k3s/storage@all --k3s-arg "--tls-san=61.101.244@server:*" --k3s-arg "--disable=traefik@server:*" --k3s-arg "--service-node-port-range=30000-30050@server:*" -p "30050:30050@loadbalancer:*" -p "80:80@loadbalancer:*" -p "443:443@loadbalancer:*" --timeout 10m
```

```
k3d kubeconfig get minio > ~/.kube/config
```

# Nginx Controller

```
helm upgrade --install ingress-nginx ingress-nginx --version 4.4.2 --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.replicaCount=1 --set controller.ingressClassResource.default=true


```

# Minio Client

```
curl https://dl.min.io/client/mc/release/linux-amd64/mc --create-dirs -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
```

# Minio Operator

```
curl https://raw.githubusercontent.com/minio/docs/master/source/extra/examples/minio-dev.yaml -O


kubectl describe pod/minio -n minio-dev

kubectl logs pod/minio -n minio-dev

 kubectl port-forward pod/minio 9000 9090 -n minio-dev
```