import subprocess
import socket
import time
from project.config import AccessPointConfig, WifiConfig, GlobalConfig


def have_internet_connection(host="8.8.8.8", port=53, timeout=2):
   """
   Returns True if we are connected to the internet, False otherwise.
   Host: 8.8.8.8 (google-public-dns-a.google.com)
   OpenPort: 53/tcp
   Service: domain (DNS/TCP)
   """
   print("check internet connection")
   try:
     socket.setdefaulttimeout(timeout)
     socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
     return True
   except Exception as e:
     return False


# COMMANDS

# RemoveApInterface removes the AP interface.

# AddApInterface adds the AP interface.
def ap_interface_add():
    print("add ap interface")
    proc = subprocess.Popen([
        "iw", "phy", "phy0", "interface", "add", AccessPointConfig.INTERFACE, "type", "__ap"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    ok = ap_interface_exists()
    if not ok:
        print("ERROR: cannot add ap interface")
    return ok

def ap_interface_remove():
    print("remove ap interface")
    proc = subprocess.Popen([
        "iw", "dev", AccessPointConfig.INTERFACE, "del"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    ok = not ap_interface_exists()
    if not ok:
        print("ERROR: cannot remove ap interface")
    return ok

def ap_interface_exists():
    print("check ap interface exists")
    proc = subprocess.Popen([
        "ifconfig", AccessPointConfig.INTERFACE],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        encoding="utf-8")
    return proc.wait() == 0

# ConfigureApInterface configured the AP interface.
def ap_interface_configure():
    print("configure ap interface")
    proc = subprocess.Popen([
        "ifconfig", AccessPointConfig.INTERFACE, AccessPointConfig.IP],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    ok = proc.wait() == 0
    if not ok:
        print("ERROR: cannot configure ap interface")
    return ok


# UpApInterface ups the AP Interface.
def ap_interface_up():
    print("ap interface UP")
    proc = subprocess.Popen([
        "ifconfig", AccessPointConfig.INTERFACE, "up"],
        stdout=subprocess.PIPE,              
        stderr=subprocess.PIPE,
        encoding="utf-8")
    ok = proc.wait() == 0
    if not ok:
        print("ERROR: cannot set ap interface UP")
    return ok

def ap_interface_down():
    print("ap interface DOWN")
    proc = subprocess.Popen([
        "ifconfig", AccessPointConfig.INTERFACE, "down"],
        stdout=subprocess.PIPE,              
        stderr=subprocess.PIPE,
        encoding="utf-8")
    ok = proc.wait() == 0
    if not ok:
        print("ERROR: cannot set ap interface DOWN")
    return ok

# StartWpaSupplicant starts wpa_supplicant.
def wpa_supplicant_start():
    wpa_supplicant_stop()
    print("start wpa_supplicant")
    args = [
        "-B",
        "-i",
        WifiConfig.INTERFACE,
        "-c",
        "{}/wpa_supplicant.conf".format(GlobalConfig.PROJECT_FOLDER)
    ]
    proc = subprocess.Popen(["wpa_supplicant"] + args,
        stdout=subprocess.PIPE,              
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    ok = wpa_supplicant_is_running()
    if not ok:
        print("ERROR: cannot start wpa_supplicant")
    return ok

def wpa_supplicant_stop():
    print("stop wpa_supplicant")
    proc = subprocess.Popen(["killall", "wpa_supplicant"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    ok = not wpa_supplicant_is_running()
    if not ok:
        print("ERROR: cannot stop wpa_supplicant")
    return ok

def wpa_supplicant_is_running():
    print("check wpa_supplicant")
    proc = subprocess.Popen(
        ["wpa_cli", "-i", WifiConfig.INTERFACE, "status"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    return proc.wait() == 0

# StartDnsmasq starts dnsmasq.
def dnsmasq_start():
    dnsmasq_stop()
    # hostapd is enabled, fire up dnsmasq
    print("start dnsmasq")
    args = [
        "--no-hosts",  # Don't read the hostnames in /etc/hosts.
        "--log-queries",
        "--no-resolv",
        "--address=/#/" + AccessPointConfig.IP,
        "--dhcp-range=" + AccessPointConfig.DHCP_RANGE,
        "--dhcp-vendorclass=set:device,IoT",
        "--dhcp-authoritative",
        "--log-facility=-",
    ]
    proc = subprocess.Popen(["dnsmasq"] + args,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        encoding="utf-8")
    ok = dnsmasq_is_runnning()
    if not ok:
        print("ERROR: cannot start dnsmasq")
    return ok

def dnsmasq_stop(check_sleep=0.5, timeout=2):
    print("stop dnsmasq")
    proc = subprocess.Popen(["killall", "dnsmasq"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    for i in range(int(timeout / check_sleep) + 1):
        if i > 0:
            time.sleep(check_sleep)
        ok = not dnsmasq_is_runnning()
        if ok:
            return True
    if not ok:
        print("ERROR: cannot stop dnsmasq")
    return ok

def dnsmasq_is_runnning():
    print("check dnsmasq is running")
    proc = subprocess.Popen(
        ["ps", "-aux"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    if proc.wait() != 0:
        return False
    std_lines = proc.stdout.read()
    return ("dnsmasq" in std_lines)

def hostapd_save_conf():
    print("save hostapd conf")
    config = """interface={}
ssid={}
channel={}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP""".format(
            AccessPointConfig.INTERFACE,
            AccessPointConfig.SSID,
            AccessPointConfig.CHANNEL,
            AccessPointConfig.PASS)
    try:
        text_file = open("hostapd.conf", "w")
        text_file.write(config)
        text_file.close()
        return True
    except Exception as e:
        print("ERROR: cannot save hostapd conf. {}".format(e))
        return False

def hostapd_start():
    ok = hostapd_stop()
    if not ok:
        return False
    ok = wpa_supplicant_start()
    if not ok:
        return False
    ok = hostapd_save_conf()
    if not ok:
        return False
    print("start hostapd")
    proc = subprocess.Popen(["hostapd", "-B", "hostapd.conf"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    stdo = proc.stdout.read()
    str_enable = "{}: AP-ENABLED".format(AccessPointConfig.INTERFACE)
    ok = str_enable in stdo
    if not ok:
        print("ERROR: cannot start hostapd")
    return ok

def hostapd_stop(check_sleep=0.5, timeout=2):
    print("stop hostapd")
    proc = subprocess.Popen(["killall", "hostapd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    proc.wait()
    for i in range(int(timeout / check_sleep) + 1):
        if i > 0:
            time.sleep(check_sleep)
        ok = not hostapd_is_running()
        if ok:
            return True
    if not ok:
        print("ERROR: cannot stop hostapd")
    return ok

def hostapd_is_running():
    print("check hostapd is running")
    proc = subprocess.Popen(
        ["ps", "-aux"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    if proc.wait() != 0:
        return False
    std_lines = proc.stdout.read()
    return ("hostapd" in std_lines)

def ap_start():
    ap_stop()
    disconnect_wifi()
    ok = ap_interface_add()
    if not ok:
        return False
    ok = ap_interface_up()
    if not ok:
        return False
    ok = ap_interface_configure()
    if not ok:
        return False
    ok = hostapd_start()
    if not ok:
        return False
    ok = dnsmasq_start()
    if not ok:
        return False
    return True

def ap_stop():
    print("stop ap")
    ok_dns = dnsmasq_stop()
    ok_hostapd = hostapd_stop()
    ok_interface = ap_interface_remove()
    return (ok_dns and ok_hostapd and ok_interface)

# Client mode

def scan_networks():
    print("scan networks")
    proc = subprocess.Popen(["wpa_cli", "-i", WifiConfig.INTERFACE, "scan"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    if proc.stdout.read() != "OK\n":
        print("ERROR: scan failed")
        return None
    proc = subprocess.Popen(["wpa_cli", "-i", WifiConfig.INTERFACE, "scan_results"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    stdo_lines = proc.stdout.readlines()
    return parse_scan_networks(stdo_lines)

def parse_scan_networks(stdout_lines):
    if len(stdout_lines) < 1:
        print("ERROR: in parse scan networks. no lines")
        return None
    try:
        networks = []
        head_list = stdout_lines[0].replace("\n", "").split(" / ")
        for net_line in stdout_lines[1:]:
            net_list = net_line.replace("\n", "").split("\t")
            net_dict = {}
            if len(head_list) != len(net_list):
                print("ERROR: parse scan network on {} with heads {}".format(net_list, head_list))
                continue
            for head, info in zip(head_list, net_list):
                net_dict[head] = info
            networks.append(net_dict)
        return networks
    except Exception as e:
        print("ERROR: parse scan network error. " + str(e))
        return None

def remove_network(net_id):
    print("remove network {}".format(net_id))
    proc = subprocess.Popen(["wpa_cli", "-i", WifiConfig.INTERFACE, "remove_network", str(net_id)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    stdo = proc.stdout.read()
    if stdo == "OK\n":
        return True
    else:
        print("ERROR: cannot remove network {}".format(net_id))
        return False

def remove_all_network():
    net_list = list_networks()
    if net_list is None:
        return True
    ret = True
    for net_id in net_list:
        ok = remove_network(net_id)
        ret = ret and ok
    return ret

def list_networks():
    print("list networks")
    proc = subprocess.Popen(["wpa_cli", "-i", WifiConfig.INTERFACE, "list_networks"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    ret = proc.wait()
    stdo_lines = proc.stdout.readlines()
    err = proc.stderr.read()
    if ret != 0:
        print("ERROR: cannot list networks")
        return None
    if len(stdo_lines) < 2:
        return []
    net_list = []
    for net_line in stdo_lines[1:]:
        try:
            net_list.append(int(net_line[0]))
        except ValueError:
            continue
    return net_list

def add_network():
    print("add network")
    proc = subprocess.Popen(["wpa_cli", "-i", WifiConfig.INTERFACE, "add_network"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    stdo = proc.stdout.read().replace("\n", "")
    try:
        return int(stdo)
    except ValueError:
        print("ERROR: cannot add new network")
        return None

def get_network_status():
    print("get network status")
    proc = subprocess.Popen(["wpa_cli", "-i", WifiConfig.INTERFACE, "status"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    stdo_lines = proc.stdout.readlines()
    status_dict = {}
    for line in stdo_lines:
        line_split = line.replace("\n", "").split("=")
        if len(line_split) < 2:
            continue
        status_dict[line_split[0]] = line_split[1]
    return status_dict

def set_network(net_id, ssid, psk, wait_status=10):
    print("set network {}: ssid={}".format(net_id, ssid))
    # set SSID
    proc = subprocess.Popen(
        ["wpa_cli", "-i", WifiConfig.INTERFACE, "set_network", str(net_id), "ssid", "\"{}\"".format(ssid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    if proc.stdout.read() != "OK\n":
        print("ERROR: cannot set network ssid")
        return False
    # set PASSWORD
    proc = subprocess.Popen(
        ["wpa_cli", "-i", WifiConfig.INTERFACE, "set_network", str(net_id), "psk", "\"{}\"".format(psk)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    if proc.stdout.read() != "OK\n":
        print("ERROR: cannot set network psk")
        return False
    # Enable network
    proc = subprocess.Popen(
        ["wpa_cli", "-i", WifiConfig.INTERFACE, "enable_network", str(net_id)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8")
    if proc.stdout.read() != "OK\n":
        print("ERROR: cannot enable network")
        return False
    # Loop for check status every sec
    for i in range(int(wait_status)):
        time.sleep(1)
        status = get_network_status()
        if status.get("wpa_state") != "COMPLETED":
            continue
        if status.get("ssid") != ssid:
            continue
        return True
    print("ERROR: connection to network failed")
    return False

def connect_wifi(ssid, psk, wait_status=10):
    disconnect_wifi()
    ap_stop()
    ok = wpa_supplicant_start()
    if not ok:
        return False
    net_id = add_network()
    return set_network(net_id, ssid, psk, wait_status)

def disconnect_wifi():
    return remove_all_network()
