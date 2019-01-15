#!/bin/bash

OLD_HOST=$(hostname)
NEW_HOST='mvimayorlamp' # Can only contain alphanumeric characters!

sudo apt-get update && sudo apt-get install git python-dev python-pip -y

read -p "Change hostname? [Y/n]" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo sh -c "echo $NEW_HOST > /etc/hostname"
	sudo sed -i "s/$OLD_HOST/$NEW_HOST/g" /etc/hosts
	printf "\nHostname set!"
fi

sudo depmod

# Set PWM pins to be used as analog audio output
echo "dtoverlay=dtoverlay=pwm-1chan,pin=13,func=2" | sudo tee -a /boot/config.txt

# Force Pi to not output audio via HDMI
sudo amixer cset numid=3 1

# Enable general SPI interface as well was enabling SPI1
printf "dtparam=spi=on\ndtoverlay=spi1-1cs" | sudo tee -a /boot/config.txt

