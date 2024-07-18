#!/bin/bash
#Ask for the IP address of the host machin
echo "Please enter the IP address of the host machine"
read ip_address
echo "export CARLA_HOST=$ip_address" >> ~/.bashrc