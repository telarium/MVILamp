#!/bin/bash



sudo apt-get install git python-dev -y

# Set PWM pins to be used as analog audio output
echo "dtoverlay=pwm-2chan,pin=18,func=2,pin2=13,func2=4" | sudo tee -a /boot/config.txt

# Force Pi to not output audio via HDMI
sudo amixer cset numid=3 2

# Need to be on at least kernel 4.4 for SPI1 interface.
sudo apt-get update && sudo apt-get -y dist-upgrade && sudo rpi-update 52241088c1da59a359110d39c1875cda56496764

# Enable general SPI interface as well was enabling SPI1
printf "dtparam=spi=on\ndtoverlay=spi1-3cs" | sudo tee -a /boot/config.txt
