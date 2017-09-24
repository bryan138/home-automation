cd /home/osmc/code/home-automation/

sudo dos2unix ./speaker-control/speaker-control.service
sudo dos2unix ./speaker-control/speaker_control.py
sudo dos2unix ./wemo-control/wemo-control.service
sudo dos2unix ./wemo-control/wemo_control.py
sudo dos2unix ./gpio-monitoring/gpio-monitoring.service
sudo dos2unix ./gpio-monitoring/gpio_monitoring.py

sudo chmod 664 ./speaker-control/speaker-control.service
sudo chmod 755 ./speaker-control/speaker_control.py
sudo chmod 664 ./wemo-control/wemo-control.service
sudo chmod 755 ./wemo-control/wemo_control.py
sudo chmod 664 ./gpio-monitoring/gpio-monitoring.service
sudo chmod 755 ./gpio-monitoring/gpio_monitoring.py

sudo cp ./speaker-control/speaker-control.service /etc/systemd/system/speaker-control.service
sudo cp ./wemo-control/wemo-control.service /etc/systemd/system/wemo-control.service
sudo cp ./gpio-monitoring/gpio-monitoring.service /etc/systemd/system/gpio-monitoring.service

sudo systemctl daemon-reload
sudo systemctl enable wemo-control.service
sudo systemctl enable gpio-monitoring.service
