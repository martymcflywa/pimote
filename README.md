# Pimote

`main.py` python script translates one remote signal (hisense-tv) to another
(smsl-ad18 amp) using a Raspberry Pi. The TV is connected to the amp via optical
cable, and can't be controlled via ARC, so this script translates power, and
volume keys from the TV remote to the amp remote.

## Prerequisites

This script assumes that LIRC is set up for the output remote and has mapped the
required keys, and that ir-keytable is installed for evdev.

# Setup

- Install lirc 0.10.2
  - See http://blog.trumpton.org.uk/2020/06/raspberry-pi-ir.html
- Install ir-keytable
  - See http://www.ignorantofthings.com/2022/03/receiving-infrared-on-raspberry-pi-with.html
- Enable all protocols for ir-keytable for rc1
  - Add this to `/etc/rc.local` before `exit 0`
  - `ir-keytable -p all -s rc1 -v`
- Add remote configs to lirc
  - Copy `lirc-config/*.lircd.conf` to `/etc/lircd/lircd.conf.d/`
- `pip install -r requirements.txt`
- Create pimote service
  - Copy `pimote.service` to `/etc/systemd/system/`
  - `sudo systemctl enable pimote.service`
  - `sudo service pimote start`
