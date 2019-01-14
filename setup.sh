#!/bin/bash

OLD_HOST=$(hostname)
NEW_HOST='mvimayorlamp' # Can only contain alphanumeric characters!

sudo apt-get install git python-dev python-pip -y

read -p "Change hostname? [Y/n]" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo sh -c "echo $NEW_HOST > /etc/hostname"
	sudo sed -i "s/$OLD_HOST/$NEW_HOST/g" /etc/hosts
	printf "\nHostname set!"
fi

sudo depmod

# Set PWM pins to be used as analog audio output
echo "dtoverlay=pwm-2chan,pin=18,func=2,pin2=13,func2=4" | sudo tee -a /boot/config.txt

# Force Pi to not output audio via HDMI
sudo amixer cset numid=3 2

# Need to be on at least kernel 4.4 for SPI1 interface.
sudo apt-get update && sudo apt-get -y dist-upgrade && sudo rpi-update 52241088c1da59a359110d39c1875cda56496764

# Enable general SPI interface as well was enabling SPI1
printf "dtparam=spi=on\ndtoverlay=spi1-3cs" | sudo tee -a /boot/config.txt

