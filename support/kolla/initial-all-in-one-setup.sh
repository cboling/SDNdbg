#!/usr/bin/env bash
#
# Copyright (c) 2015 - Present.  Boling Consulting Solutions, BCSW.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#######################################################################
# Script to create a local Kolla instance for OpenStack Deployments
#######################################################################
# A few useful environment variables

KOLLA_INVENTORY=${SDNDBG_BASE}/support/kolla/inventory
KOLLA_SHARE=${VIRTUAL_ENV}/share/kolla-ansible
CONFIG_DIR=${SDNDBG_BASE}/support/config/all-in-one-dev
#
# Make sure some require packages are available. Most python packages should
# have already been installed into the local virtual environment
#
sudo apt update || exit 1
sudo apt install -y ansible python-dev libffi-dev gcc libssl-dev python-selinux \
                  lsb-release software-properties-common python-software-properties || exit 1

# Tweek the /etc/ansible/ansible.cfg file
#[defaults]
#host_key_checking=False
#pipelining=True
#forks=100
sudo cp /etc/ansible/ansible.cfg /etc/ansible.cfg.bak || exit 2
sudo sed --in-place 's/#host_key_checking/host_key_checking/' /etc/ansible/ansible.cfg || exit 2
sudo sed --in-place 's/#pipelining[[:blank:]]*=[[:blank:]]*False/pipelining=True/' /etc/ansible/ansible.cfg || exit 2
sudo sed --in-place 's/#forks[[:blank:]]*=[[:blank:]]*5/forks=100/' /etc/ansible/ansible.cfg || exit 2

# Install kolla-ansible
pip install kolla-ansible || exit 2
sudo cp -r ${KOLLA_SHARE}/etc_examples/kolla/* /etc/kolla/ || exit 3

# Get a copy of the inventory examples
mkdir -p ${KOLLA_INVENTORY} || exit 4
cp -r ${KOLLA_SHARE}/ansible/inventory/* ${KOLLA_INVENTORY}/ || exit 4

# Backup configuration and then edit the Kolla Configuration
sudo mv -f /etc/kolla/globals.yml /etc/kolla/globals.yml.dist || exit 5
sudo mv -f /etc/kolla/passwords.yml /etc/kolla/passwords.yml.dist || exit 5
sudo cp ${CONFIG_DIR}/globals.yml /etc/kolla/globals.yml || exit 5
sudo cp ${CONFIG_DIR}/passwords.yml /etc/kolla/passwords.yml || exit 5

# Nova setup
sudo mkdir -p /etc/kolla/config/nova || exit 6
sudo cp ${CONFIG_DIR}/nova-compute.conf /etc/kolla/config/nova || exit 6

# Network setup
# eth1 should be a private network for use as the OpenStack API/Control network
# eth2 should be an external network (in promisc mode if on VM) for Neutron
#sudo ${CONFIG_DIR}/eth1 /etc/network/interfaces.d/
#sudo ${CONFIG_DIR}/eth2 /etc/network/interfaces.d/

# Password generation
sudo kolla-genpwd

# We are targeting OpenStack Pike or later. The python 'docker' library is needed
# but not the 'docker-py' (Ocata and previous) due to conflicts

#sudo pip uninstall docker-py || exit 7
#sudo pip install -U docker || exit 7

###################################################################################
# Touch up default/main.yaml to not customize the etc/hosts file
# NOTE: Only use this if running inside a docker container at this point
#
# sudo sed --in-place 's/^customize_etc_hosts/#customize_etc_hosts/' ${KOLLA_SHARE}/ansible/roles/baremetal/defaults/main.yml
# sudo sed --in-place '/^#customize_etc_hosts*/acustomize_etc_hosts: False' ${KOLLA_SHARE}/ansible/roles/baremetal/defaults/main.yml
#
###################################################################################
#
# Bootstrap the server (use -vvv line below for extra debug)
#
#  NOTE: You may want to tweek the docker version listed in ${KOLLA_SHARE}/ansible/roles/baremetal/defaults/main.yml
#        to at least be your local version (at least later than what is listed).  Note that
#        docker-ce reports as docker-engine but leaves the prefix 1.* off.
#
# kolla-ansible -vvv -i ${KOLLA_INVENTORY}/all-in-one bootstrap-servers
kolla-ansible -i ${KOLLA_INVENTORY}/all-in-one bootstrap-servers

# Seed the docker images
kolla-ansible pull

# Success if here
echo "Successfully initial install of all-in-one Kolla"
echo
echo "To deploy OpenStack enter the following command, and then check docker container status"
echo "with 'docker ps -a"
echo
echo "  sudo -E kolla-ansible deploy -i ${KOLLA_INVENTORY}/all-in-one"
exit 0