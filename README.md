# RemoteSystemControl

Simple set of classes to control my audio system (can be suitable for any IR/Radio controlled system). Includes: web-server on python, LIRC config file and Android app.

To run standalone server:
```
python RemoteControlWebCore.py
```
To run as balena docker:
```
version: '2'
volumes:
  resin-data:
services:
  speaker-control:
    build: ./speaker-control
    restart: always
    network_mode: host
    privileged: true
    volumes:
      - 'resin-data:/data'
```
Don't forget to add dtoverlay in both cases:
```
"gpio-ir-tx","gpio_pin=22"
```
