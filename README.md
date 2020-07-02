# Raspi Wifi API

API to control Wifi network on your Raspberry Pi. Ideal for IoT projects.

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
git clone https://github.com/alexisthethe/raspi-wifi-api.git
```

```
cd raspi-wifi-api
./scripts/install_api.sh
```


## Usage

API is hosted on port `5678`, then the API is available at the address http://<raspi_ip>:5678/


### First connection

When the app is launched for the first time, the raspberry pi is on AP (Access Point) mode.
You can connect to its AP wifi with the SSID and password you configurated. By default, if not configurate SSID is `raspi-hotspot` and password is `rpipass8*`.
The <raspi_ip> of the device is the one you configurate. By default, this is `192.168.27.1` and the API is available at the address [http://192.168.27.1:5678](http://192.168.27.1:5678).

### API Routes

* */internet_status*

Check if the raspberry pi has access to internet
response :
Internet
```json
{"status": true/false}
```

* */netscan*

Scan surrounding WiFi networks and returns SSIDs as a list
```json
["SSID1", "SSID2", "wifissid"]
```

* */start_ap*

Switch to AP mode

* */stop_ap*

Stop AP mode

* */connect_wifi*

Connect to an external wifi
Parameters *ssid* and *psk*
Example: */connect_wifi?ssid=yourssid&psk=yourpass*

* */disconnect_wifi*

Disconnect from the connected external wifi

* */wifi_status*

Return WiFi status and information
