#!/bin/bash
#Copyright (C) 2018-2021 Intel Corporation
#SPDX-License-Identifier: Apache-2.0
sudo apt-get update
sudo apt-get install expect -y
export HOST_IP=$(hostname -I | cut -d' ' -f1)
sudo docker pull intel/intelligent_traffic_management:4.0
sudo docker pull influxdb:1.8
echo "Installing edgesoftware ..."
pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo $HOST_IP
/usr/bin/expect -c '
set timeout -1
spawn $::env(HOME)/.local/bin/edgesoftware install wireless-network-ready-intelligent-traffic-management 623c98999654a8f4bd94f55b
expect "download:" {send "04b8af94-ecea-4377-bf8c-19592d3ac4f7\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send $::env(HOST_IP)\r"}
expect EOF'

echo -e "\e[1;32m\n********* Generating Grafana Password **************\e[0m"
echo -e "\e[1;33mCopy paste the token in grafana dashboard \e[0m\n"
kubectl get secrets/grafana -n telemetry -o json | jq -r '.data."admin-password"' | base64 -d
echo -e "\n\n"
HOST_IP=$(hostname -I | awk '{print $1}')

echo -e "\e[1;32m\n********* Grafana URL **************\e[0m"
#kubectl get secrets/grafana -n telemetry -o json | jq -r '.data."admin-password"' | base64 -d
echo -e "\e[1;36mGrafana Dashboard is available in the below URL\e[0m"
echo -e "\e[1;33mhttps://$HOST_IP:32000 \e[0m\n"

