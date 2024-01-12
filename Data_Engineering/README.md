# Installation Of Krew

The 'krew' package is a manager for kubectl plugins. It allows you to easily install kubectl plugins. How to intall krew?

```
# 1. Run this command to download and install krew:
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)

# 2. Append the $HOME/.krew/bin directory to your PATH environment variable.
# To do this, update your .bashrc or .zshrc file and append the following line:

nano ~/.bashrc

export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
```

# K3s - Install and Configs

K3s is a certified Kubernetes distribution specifically crafted for production workloads. It is designed to operate effectively in unattended, resource-constrained, remote locations, or within IoT appliances, ensuring high availability.

```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable traefik" K3S_KUBECONFIG_MODE="644" INSTALL_K3S_SKIP_START=true  sh -s -

sudo systemctl start k3s

# Copy the config file to the default location where kubectl looks for that.
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
```

# Installing K3d


K3d serves as a lightweight wrapper for executing k3s, which is Rancher Lab's minimal Kubernetes distribution, within a Docker environment. It simplifies the process of establishing both single- and multi-node k3s clusters in Docker, facilitating local Kubernetes development.

How to install k3d:

```

```

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