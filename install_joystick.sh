#!/bin/env bash
# Install prerequisite packages
sudo apt-get install -y  libusb-dev joystick python-pygame
# Get the library to pair
mkdir sixpair
cd sixpair
wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair sixpair.c -lusb
