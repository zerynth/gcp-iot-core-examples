# -*- coding: utf-8 -*-
# @Author: Lorenzo
# @Date:   2018-10-05 14:39:52
# @Last Modified by:   Lorenzo
# @Last Modified time: 2018-10-05 16:01:04
"""
Provision the kit to make example projects ready to be compiled and uplinked.
"""

import sys
import os
import json
import click

ZERYNTH_PROJECT_NAME = "GoogleCloudConnect"
DEVICE_CONF_FILE = "device.conf.json"
CRYPTO_SCAN_FILE = "scanned_crypto.json"

def alloptionsrequired(function):
    """
    Decorator to make all click options required.
    Option should be optional, but they cannot be arguments.
    """
    def require_options_fn(**kwargs):
        for option, _ in kwargs.items():
            if not kwargs[option]:
                print('Error: missing option "%s", --help for available options' % option)
                sys.exit()
        function(**kwargs)
    return require_options_fn

@click.command()
@click.option('--ssid', 'wifi_ssid', help='WiFi SSID, REQUIRED')
@click.option('--password', 'wifi_password', help='WiFi Password, REQUIRED')
@click.option('--device_id', help='Google Cloud IoT Core Device ID, REQUIRED')
@click.option('--registry_id', help='Google Cloud IoT Core Registry ID, REQUIRED')
@click.option('--project_id', help='Google Cloud Project ID, REQUIRED')
@click.option('--cloud_region', help='Google Cloud Project Region, REQUIRED')
@alloptionsrequired
def provision(**kwargs):
    """
    Join passed options and scanned crypto info to built project device configuration.
    """
    print('Read device configuration.')
    with open(os.path.join(ZERYNTH_PROJECT_NAME, DEVICE_CONF_FILE)) as conf_read:
        devconf = json.loads(conf_read.read())

    print('Read scan output.')
    with open(CRYPTO_SCAN_FILE) as crypto_scan:
        scan_info = json.loads(crypto_scan.read())

    devconf.update({'i2caddr': scan_info['address'], 'devtype': scan_info['devtype']})
    devconf.update(kwargs)
    with open(os.path.join(ZERYNTH_PROJECT_NAME, DEVICE_CONF_FILE), 'w+') as conf_write:
        conf_write.write(json.dumps(devconf, indent=4, sort_keys=True))

    print('Device configuration updated.')
    print('Kit successfully Provisioned.')

if __name__ == '__main__':
    # pylint: disable=E1120
    provision()
