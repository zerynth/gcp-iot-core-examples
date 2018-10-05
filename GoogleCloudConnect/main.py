# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2018-08-24 11:27:40
# @Last Modified by:   Lorenzo
# @Last Modified time: 2018-10-05 15:34:59

import streams

from microchip.ateccx08a import ateccx08a
from microchip.winc1500 import winc1500 as wifi_driver
from googlecloud.iot import iot

from wireless import wifi

import helpers

# define a callback for config updates
def config_callback(config):
    global sampling_period
    if 'sampling_period' in config:
        print('requested sampling period:', config['sampling_period'])
        sampling_period = config['sampling_period']
    if 'led_state' in config:
        digitalWrite(LED0, LOW if config['led_state'] == 'on' else HIGH)
    return config

pinMode(LED0, OUTPUT)
digitalWrite(LED0, HIGH)

streams.serial()
new_resource('device.conf.json')
device_conf = helpers.load_device_conf()

wifi_driver.auto_init(ext=1)
wifi.link(device_conf['wifi_ssid'], wifi.WIFI_WPA2, device_conf['wifi_password'])
print('> linked')

sampling_period = 2000
ateccx08a.hwcrypto_init(I2C0, 2, i2c_addr=device_conf['i2caddr'], dev_type=helpers.conf2atecctype[device_conf['devtype']])

# create a google cloud device instance, connect to mqtt broker, set config callback and start mqtt reception loop
device = iot.Device(device_conf['project_id'], device_conf['cloud_region'], device_conf['registry_id'], device_conf['device_id'], '', helpers.get_timestamp, custom_jwt=ateccx08a.encode_jwt)
print('> mqtt connect')
device.mqtt.connect()
print('> connected')

device.on_config(config_callback)

while True:
    print('> publish sample.')
    rand_val = random(0,10)
    device.publish_event({'rand': rand_val})
    sleep(sampling_period)

