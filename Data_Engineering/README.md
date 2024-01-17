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
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

```


# Create volume

```
mkdir -p /server/k3d
chmod 777 /server/k3d
```


# Create cluster

```
k3d cluster create minio --servers 3 --agents 3 -v /server/k3d:/var/lib/rancher/k3s/storage@all --k3s-arg "--tls-san=61.101.244@server:*" --k3s-arg "--disable=traefik@server:*" --k3s-arg "--service-node-port-range=30000-30050@server:*" -p "30050:30050@loadbalancer:*" -p "80:80@loadbalancer:*" -p "443:443@loadbalancer:*" --timeout 10m

k3d cluster create onion-dev --servers 1 --agents 2 -v /home/wesley/server/k3d:/var/lib/rancher/k3s/storage@all --k3s-arg "--tls-san=192.168.0.147@server:*" --k3s-arg "--disable=traefik@server:*" --k3s-arg "--service-node-port-range=30000-30050@server:*" -p "30050:30050@loadbalancer:*" -p "80:80@loadbalancer:*" -p "443:443@loadbalancer:*" --timeout 10m

sudo kubectl cluster-info

# check memory usage
free -h

# check disk usage
df -h

# Cpu usage
top
```

```
k3d kubeconfig get minio > ~/.kube/config
```

# Installation of DirectPV on K3s

[DirectPV](https://github.com/minio/directpv?tab=readme-ov-file) functions as a CSI driver specifically crafted for Direct Attached Storage, acting as a distributed persistent volume manager that sets it apart from storage systems like SAN or NAS. Its practicality extends to detecting, formatting, mounting, scheduling, and monitoring drives across multiple servers.

Direct-attached storage (DAS) refers to digital storage directly connected to the computer in use, in contrast to storage accessed via a computer network (such as network-attached storage). DAS comprises one or more storage units like hard drives, solid-state drives, and optical disc drives housed within an external enclosure. The term "DAS" is a retronym, highlighting the distinction from storage area network (SAN) and network-attached storage (NAS).

```
# Install DirectPV Krew plugin
kubectl krew install directpv

# Install DirectPV in your kubernetes cluster
kubectl directpv install

# Get information of the installation
kubectl directpv info

# Add drives

## Probe and save drive information to drives.yaml file.
kubectl directpv discover

## Initialize selected drives.
## you van create a yaml file with the configs
cat drives.yaml
kubectl directpv init drives.yaml
kubectl directpv init drives.yaml --dangerous
kubectl directpv list drives

# Deploy a demo MinIO server
curl -sfL https://github.com/minio/directpv/raw/master/functests/minio.yaml | kubectl apply -f -
```

## Fixing CSI bugs

```
kubectl get pods -n directpv
kubectl logs -n directpv node-server-hq8tq
kubectl exec -n directpv node-server-hq8tq -- ls /csi
kubectl logs -n directpv node-server-hq8tq -c directpv-min-io
```

# Installation of Ingress Nginx

[Ingress Nginx](https://kubernetes.github.io/ingress-nginx/deploy/) is an Ingress controller for kubernetes using Nginx as a reverse proxy and load balancer. It is the most popular Ingress controller for kubernetes. He is reliable and easy to use, providing load balancing, SSL termination, and name-based virtual routing features.
However, it does not support dynamic configurations, so an NGINX reload is required whenever a new Kubernetes endpoint is defined.The ingress controller is for pointing DNS names to our cluster and then routing them to the proper pods inside the cluster. So this is HTTP and HTTPS traffic only.

```
helm upgrade --install ingress-nginx ingress-nginx --version 4.4.2 --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.replicaCount=1 --set controller.ingressClassResource.default=true

kubectl get ingressclass
kubectl get pods -A
kubectl get pods --namespace=ingress-nginx
```

# Minio Client

The MinIo Client is a command-line tool for interacting with MinIo Object Storage and other S3-compatible Object Storage systems.

```
curl https://dl.min.io/client/mc/release/linux-amd64/mc --create-dirs -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
```

# Kubernetes Options for MinIO

MinIO can run on any Kubernetes cluster that supports all of the common Kubernetes features and is API compatible with upstream Kubernetes.

Some examples of supported Kubernetes distributions include:

- Amazon Elastic Kubernetes Service (EKS)
- Google Kubernetes Engine (GKE)
- Azure Kubernetes Service (AKS)
- Red Hat OpenShift Container Platform (OCS)
- Rancher, k3s, RKE, and RKE2

## Deploying MinIO on Kubernetes using Manifest Files

We will deploy a Single-Node Single-Drive MinIO server onto Kubernetes for early development and evaluation of MinIO Object Storage and its S3-compatible API Layer. And, We will use the MinIO Operator to deploy and manage production-ready MinIO tenants on Kubernetes. 

```
# download basic yaml
curl https://raw.githubusercontent.com/minio/docs/master/source/extra/examples/minio-dev.yaml -O

# deploy minio application
kubectl apply -f minio-dev.yaml

kubectl get ns
kubectl get pods -n minio-dev

# retrieving detailed pod status information

kubectl describe pod/minio -n minio-dev

kubectl logs pod/minio -n minio-dev

# 
kubectl port-forward pod/minio 9000 9090 -n minio-dev
```

## How to Fix the ImagePullBackOff Error

- Step 1: Collect information
```
kubectl get pods
kubectl describe pod minio -n minio-dev
```
- We have a DNS connection problem
```
# To get the core-dns name
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Cluster-Wide DNS Service Logs:
kubectl logs -n kube-system coredns-77ccd57875-bnqh6
kubectl logs -n kube-system coredns-77ccd57875-bnqh6 > Data_Engineering/logs/coredns_logs.txt

# Config Service to browser interaction

```
kubectl apply -f minio-dev-nodeport.yaml
```