# Zerynth Microchip Examples for Google Cloud Platform IoT Core

## Summary

This project contains examples and tools for setting up a secure IoT node with IoT Core
using the ATECC508A or ATECC608A and WINC1500 with a selection of energy efficent microcontrollers.

### Software Setup

Install [**Zerynth Studio**](https://www.zerynth.com/zerynth-studio/).

### Security Devices:
* [ATECC508A](http://www.microchip.com/wwwproducts/en/ATECC508A)
* [ATECC608A](http://www.microchip.com/wwwproducts/en/ATECC608A)

### Connectivity:
* [ATWINC1500](http://www.microchip.com/wwwproducts/en/ATWINC1500) - 802.11 b/g/n Module with integrated TLS 1.2 stack
* [ATSAMW25](http://www.microchip.com/wwwproducts/en/ATSAMW25) - Integrated module featuring ATWINC1500 + ATSAMD21G18A + ATECC508A

### Microcontroller Devices:
* ATSAMD21    (ARM Cortex-M0+)
* ATSAMG55    (ARM Cortex-M4)
* ATSAMW25    (ARM Cortex-M0+)

### Getting Started

The first step is ensuring that you have a [Google Cloud IoT Core](https://console.cloud.google.com) account set up with IoT core.
The tutorials will walk you through the initial configuration of your account and creation of your first device registry and device.

1) [IoT Core Getting Started Guide](https://cloud.google.com/iot/docs/how-tos/getting-started)
2) [IoT Core Quick start](https://cloud.google.com/iot/docs/quickstart)

Zerynth Python binary can be used to execute the demo custom Python scripts without further dependencies. 
Run ``ztc info --tools`` to retrieve Python path. (e.g. C:\Users\myusername\zerynth2\sys\python\python.exe)
Zerynth Python binary called ZERYNTH_PYTHON henceforth.

### Provision the ATECCx08A on the kit

1. Register and virtualize the device.
2. Run ```ztc device discover --matchdb``` to retrieve the device uid.
3. Run ```ztc device alias put RETRIEVEDUID gcp_board USEDDEVICE```, where ```USEDDEVICE``` can be one of ```xplained_samg55```, ```xplained_d21```, ```arduino_mkr1000```,  to assign the alias ```gcp_board``` to the device (```--classname ArduinoMKR1000``` is also needed for ```arduino_mkr1000``` target).
4. Run ```ztc provisioning uplink-config-firmware gcp_board --i2caddr 0x0``` to prepare the device for provisioning.
5. Run ```ztc provisioning crypto-scan gcp_board -o .``` to obtain address and type of the crypto element (stored to configure the application).
6. Run ```ztc provisioning write-config gcp_board configuration.bin --lock True``` to write desired configuration to the device. **This command LOCKS the crypto element and sets the address to 0x58, this procedure is IRREVERSIBLE**
7. Manually reset the device and run again ```ztc provisioning crypto-scan gcp_board -o .``` to check if the new address has been assigned and to update scanned info file.
8. Run ```ztc provisioning gen-private gcp_board 2``` to generate a private key inside slot 2 of the crypto element.
9. Run ```ztc provisioning get-public gcp_board 2 -o devpublic.pem``` to generate a private key inside slot 2 of the crypto element.
10. Run ```ZERYNTH_PYTHON kit_provision.py --ssid WIFI-NAME --password WIFI-PSW --device_id DEVID --registry_id REGISTRYID --cloud_region=REGION --project_id=PROJECTID``` to update the Zerynth project device configuration file.

### Register retrieved public key on Google Cloud

1. If you have [Google Cloud CLI](https://cloud.google.com/pubsub/docs/quickstart-cli) installed and configured on your system simply run ```gcloud iot devices credentials create --path=devpublic.pem --type=es256 --device=DEVID --region=REGION --registry=REGISTRYID --project=PROJECTID```, otherwise manually paste ```devpublic.pem``` content in the text box that appears under your device page on Goolge Cloud IoT Core console after pressing ```Add public key``` and selecting ```Enter manually``` as ```Input method``` and ```ES256``` as ```Public key format```.

### Uplink Zerynth Project

1. Open Zerynth Studio.
2. **From the Device Management Widget switch to Advanced Mode and then back to Auto mode to force alias refresh.**
3. Open GoogleCloudConnect project.
4. Open the serial monitor to see, after uplink, if the device successfully connects to the WiFi and to the cloud.
Uplink the project.

### Poll Device Messages

1. Create a subscription to collect mqtt data into a Google Cloud PubSub queue via ```gcloud pubsub subscriptions create``` command or Google Cloud Console.
2. [Set Google Cloud credentials for your environment](https://cloud.google.com/docs/authentication/getting-started) and run ```ZERYNTH_PYTHON at_gui.py SUBSCRIPTION``` to see incoming data. Update publish period and led state from the console via device's config.

## Releases

### 2018-10-05

- Initial release
