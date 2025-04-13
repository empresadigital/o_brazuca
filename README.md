# o_brazuca - Gran Turismo 7 Telemetry Reader

A simple Python script to read and display Gran Turismo 7 (GT7) telemetry data from a PS5 via UDP.

Windows Firewall initially blocked UDP 33740 packets. After resetting the firewall (netsh advfirewall reset) and allowing Python via a prompt, we added a precise rule:

netsh advfirewall firewall add rule name="GT7 Telemetry" dir=in action=allow protocol=UDP localport=33740 localip=192.168.100.3 remoteip=192.168.100.27 profile=any program="...\Scripts\python.exe"

## Purpose
Captures GT7 telemetry (e.g., speed, gear, RPM) sent over UDP from a PS5 to a Windows PC, displaying it in the terminal at a human-readable pace.

## Setup
- **Python:** 3.11+
- **Dependencies:** `salsa20` (`pip install salsa20`)
- **PS5 IP:** `192.168.100.27` (update in `main.py` if different)
- **PC IP:** `192.168.100.3` (update in `main.py` if different)
- **Ports:** Send: 33739, Receive: 33740

### Virtual Environment
```cmd
py -3.11 -m venv venv
venv\Scripts\activate
pip install salsa20
