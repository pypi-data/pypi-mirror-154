#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

export HOST_IP=$(hostname -I | cut -d' ' -f1)

if [[ $(which docker) && $(docker --version) ]]; then
         echo "Docker is installed "
     else
         echo "Install docker from devtool"
         # command
         #sudo apt-get remove docker docker-engine docker.io containerd runc
fi

#install kubeadm
if [[ $(which kubeadm) && $(sudo kubeadm version) ]]; then
         echo "kubeadm is installed"
     else
         echo "installing kubeadm....."
         echo
         sudo mkdir /etc/docker
         cat <<EOF | sudo tee /etc/docker/daemon.json
         {
          "exec-opts": ["native.cgroupdriver=systemd"],
          "log-driver": "json-file",
          "log-opts":  {
          "max-size": "100m"
          },
          "storage-driver": "overlay2"
         }
         EOF
         sudo systemctl enable --now docker
         sudo systemctl daemon-reload
         sudo systemctl restart docker
         sudo systemctl status docker
         sudo groupadd docker
         sudo usermod -aG docker $USER
         echo "Disabling swap"
         sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
         sudo swapoff -a
         echo "Updating iptables"
         cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
         br_netfilter
         EOF
         cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
         net.bridge.bridge-nf-call-ip6tables = 1
         net.bridge.bridge-nf-call-iptables = 1
         EOF
         echo "Install Kubectl and Kubernetes"
         sudo apt-get update -y
         sudo apt-get install -y apt-transport-https ca-certificates curl
         sudo sysctl --system
         sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
         echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
         echo "Update apt package"
         sudo apt-get update
         sudo apt-get install -y kubelet kubeadm kubectl
         sudo apt-mark hold kubelet kubeadm kubectl
         echo "Initializing kubeadm"
         sudo kubeadm init --ignore-preflight-errors=all --pod-network-cidr=172.31.28.0/24
         kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
         GITHUB_URL=https://github.com/kubernetes/dashboard/releases
         VERSION_KUBE_DASHBOARD=$(curl -w '%{url_effective}' -I -L -s -S ${GITHUB_URL}/latest -o /dev/null | sed -e 's|.*/||')
         kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/${VERSION_KUBE_DASHBOARD}/aio/deploy/recommended.yaml
         kubectl patch svc kubernetes-dashboard -n kubernetes-dashboard --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
         kubectl patch svc kubernetes-dashboard -n kubernetes-dashboard --type='json' -p '[{"op":"replace","path":"/spec/ports/0/nodePort","value":30050}]'
         kubectl get svc -n kubernetes-dashboard -o go-template='{{range .items}}{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{"\n"}}{{end}}{{end}}{{end}}'
         echo "ClusterIP replaced with NodePort"
         NODE_PORT=`sudo k3s kubectl get svc -n kubernetes-dashboard -o go-template='{{range .items}}{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{"\n"}}{{end}}{{end}}{{end}}'`
         echo -e "\e[1;36mIt will take couple of minutes for the kubeadm server to start up\e[0m"
         echo -e "\e[1;33mInstalled kubeadm successfully, Control Plane can be accessed by clicking https://"$HOST_IP":"$NODE_PORT"\e[0m"
fi
