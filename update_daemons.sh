cd /media/USB_8/home-automation

dos2unix ./speaker-control/speaker-control.sh
dos2unix ./speaker-control/speaker_control.py
dos2unix ./wemo-control/wemo-control.sh
dos2unix ./wemo-control/wemo_control.py
dos2unix ./gpio-monitoring/gpio-monitoring.sh
dos2unix ./gpio-monitoring/gpio_monitoring.py

chmod 755 ./speaker-control/speaker-control.sh
chmod 755 ./speaker-control/speaker_control.py
chmod 755 ./wemo-control/wemo-control.sh
chmod 755 ./wemo-control/wemo_control.py
chmod 755 ./gpio-monitoring/gpio-monitoring.sh
chmod 755 ./gpio-monitoring/gpio_monitoring.py

cp ./speaker-control/speaker-control.sh /etc/init.d/speaker-control.sh
cp ./wemo-control/wemo-control.sh /etc/init.d/wemo-control.sh
cp ./gpio-monitoring/gpio-monitoring.sh /etc/init.d/gpio-monitoring.sh

update-rc.d speaker-control.sh defaults
update-rc.d wemo-control.sh defaults
update-rc.d gpio-monitoring.sh defaults
