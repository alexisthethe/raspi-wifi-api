# Raspi Wifi API

API to control Wifi network on your Raspberry Pi. Ideal for IoT projects

## Install on your raspberry pi

### Method 1: Docker

First `ssh` into your Raspberry Pi.

#### Install Docker

```
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get autoremove -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
sudo usermod -aG docker pi
```

#### Setup network config

Activate wlan0
```
sudo rfkill unblock wifi
```

Install hostapd
```
sudo apt-get install hostapd
```

Install dnsmasq
```
sudo apt-get install dnsmasq
```

Reinstall wpasupplication
```
sudo apt-get install --reinstall wpasupplicant
```

Disable dnsmasq at start
```
sudo systemctl disable dnsmasq.service
```

Disable wpa_supplicant at start
```
sudo systemctl mask wpa_supplicant.service
sudo mv /sbin/wpa_supplicant /sbin/no_wpa_supplicant
sudo pkill wpa_supplicant
```

Reboot your Raspberry Pi
```
sudo reboot
```

#### Download the docker image

Once the Raspberry Pi has reboot, download the docker image


### Method 2: native API 

Clone the repo directly on the raspberry pi or on your local machine and use `scp` to copy on the raspberry pi
```
git clone git@github.com:alexisthethe/raspi-wifi-api.git
```

```
cd raspi-wifi-api
./scripts/install_api.sh
```

## Usage
