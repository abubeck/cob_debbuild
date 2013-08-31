#!/usr/bin/env bash

echo "deb http://packages.ros.org/ros/ubuntu precise main" > /etc/apt/sources.list.d/ros-latest.list
wget http://packages.ros.org/ros.key -O - | apt-key add -
apt-get update

apt-get install -y ros-hydro-catkin ros-hydro-rospack ros-groovy-catkin ros-groovy-rospack dh-make git-buildpackage python-yaml curl wget git-buildpackage openjdk-7-jre

ln -fs /vagrant_data /home/vagrant/cob_debbuild