# home-automation
Basic set of script intended to provide home automation services using Alexa, Raspberry Pi and other technologies

## Modules

#### speaker-control
Designed to link the power-on event of a PC with a set of speakers using a Raspberry Pi. When initiated, this module will power both the PC (using wake-on-lan) and the speakers (using a relay module), and proceed to poll the system to see if it's still on, by sending pings every _n_ seconds. When the PC is no longer on, it will proceed to power off the speakers.

#### gpio-monitoring
Polling system to detect a physical button press and execute custom actions

#### wemo-control
Emulation of wemo devices to allow control over Amazon's Alexa. Fauxmo emulation from: https://github.com/toddmedema/echo (Thanks!)
