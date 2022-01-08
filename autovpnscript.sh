
#!/bin/bash
# set -x auskommentieren fuer den Debug Modus. Die Ausgabe erscheint in der Kommandozeile.
#set -x

#credits to: http://www.kuemmel-digital.com/?p=363 and commenters

# hier wird die Logfile-Datei definiert
# Logfile muss erst mit "sudo touch fritzbox.log" am Zielort erstellt werden

LOGFILE=/dev/null
#/var/log/fritzbox.log
VPN_FILE=fritzbox.conf

# hier wird die IP-Adresse der  Fritzbox definiert. Wenn die VPN Verbindung steht, dann sollte ping funktionieren.
myHost=192.168.178.1
# Wert -> wie oft soll gepingt werden
wert=4
# Ausgabe Wert fuer "count" soll bei erfolgreichen ping 4 sein, bei erfolglosen ping 0.
count=$(ping -c $wert $myHost | grep "received" | awk '{print $4 }')
if [ $count -eq 4 ]
then
    # die kommenden echos sind die Info-Ausgaben in Logfile
    echo "$(date +%Y-%m-%d:%T) :Fritzbox mit der IP $myHost ist erreichbar und VPN Verbindung steht"
else
    echo "$(date +%Y-%m-%d:%T) :Fritzbox mit der IP $myHost ist nicht erreichbar"
    echo "$(date +%Y-%m-%d:%T) :VPN-Verbindung trennen"

    #hier wird das VPNC-Demon gestoppt, damit es nicht mehr im Hintergrund lauft
    /usr/sbin/vpnc-disconnect
    # oft ist die Wlan Verbindungen unterbrochen. hier werden alle Netzwerkverbindungen neugestartet.
    echo "$(date +%Y-%m-%d:%T) :Netzwerkverbindungen neu starten"
    service network-manager restart
    # 12 Sekunden warten
    sleep 12
    # auslesen der Wlan Ip-Adresse
    # grep Adresse muss bei Englischen Spracheinstellungen evtl. geÃ¤ndert werden. Mit dem Debug Modus ausprobieren
    ipwlan=$(/sbin/ifconfig wlan0 | grep "inet" | cut -b 14-29)
    echo "$(date +%Y-%m-%d:%T) :Netzwerkverbindungen wurde neugestart. WLAN IP-Adresse: $ipwlan " | tee -a $LOGFILE
    echo "$(date +%Y-%m-%d:%T) :VPN Verbindung neu aufbauen, fritzbox.conf laden" | tee -a $LOGFILE

    # starten von VPNC-Demon. PID und VPN-IP Adresse auslesen
    /usr/sbin/vpnc $VPN_FILE
    pid=$(pidof vpnc)

    ipvpn=$(/sbin/ifconfig tun0 | grep "inet" | cut -b 14-29)
    echo "$(date +%Y-%m-%d:%T) :Die VPN-Verbindung wurde erfolgreich aufgebaut. VPNC-Demon ist aktiv unter id: $(pidof vpnc)"
    echo "$(date +%Y-%m-%d:%T) :VPN IP-Adresse: $ipvpn " | tee -a $LOGFILE
fi
