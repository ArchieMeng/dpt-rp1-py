import argparse
import base64
import sys
import json

from dptrp1 import DigitalPaper

def do_screenshot(d, filename):
    pic = d.take_screenshot()
    with open(filename, 'wb') as f:
        f.write(pic)

def do_list_documents(d):
    data = d.list_documents()
    for d in data:
        print(d['entry_path'])

def do_upload(d, local_path, remote_path):
    with open(local_path, 'rb') as fh:
        d.upload(fh, remote_path)

def do_download(d, remote_path, local_path):
    data = d.download(remote_path)

    with open(local_path, 'wb') as f:
        f.write(data)

def do_new_folder(d, remote_path):
    d.new_folder(remote_path)

def do_wifi_list(d):
    data = d.wifi_list()
    print(json.dumps(data, indent=2))

def do_wifi_scan(d):
    data = d.wifi_scan()
    print(json.dumps(data, indent=2))

def do_wifi(d):
    print(d.wifi_enabled()['value'])

def do_wifi_enable(d):
    print(d.enable_wifi())

def do_wifi_disable(d):
    print(d.disable_wifi())

def do_add_wifi(d):
    print(d.configure_wifi(ssid = "vecna2",
                     security = "psk",
                     passwd = "elijah is a cat",
                     dhcp = "true",
                     static_address = "",
                     gateway = "",
                     network_mask = "",
                     dns1 = "",
                     dns2 = "",
                     proxy = "false"))

def do_delete_wifi(d):
    print(d.delete_wifi(ssid = "vecna2", security = "psk"))

def do_register(d):
    d.register()

if __name__ == "__main__":

    commands = {
        "screenshot": do_screenshot,
        "list-documents" : do_list_documents,
        "upload" : do_upload,
        "download" : do_download,
        "new-folder" : do_new_folder,
#        "list-folders" : do_list_folders,
        "wifi-list": do_wifi_list,
        "wifi-scan": do_wifi_scan,
        "wifi-add": do_add_wifi,
        "wifi-del": do_delete_wifi,
        "wifi": do_wifi,
        "wifi-enable" : do_wifi_enable,
        "wifi-disable" : do_wifi_disable,
        "register" : do_register
    }

    def build_parser():
        p = argparse.ArgumentParser(description = "Remote control for Sony DPT-RP1")
        p.add_argument('--client-id', 
                help = "Client id of the device (or the file it's in)",
                required = True)
        p.add_argument('--key-file', 
                help = "File containing the device's private key",
                required = True)
        p.add_argument('--addr', 
                help = "IP address of the device")
        p.add_argument('command', 
                help = 'Command to run', 
                choices = sorted(commands.keys()))
        p.add_argument('command_args',
                help = 'Arguments for the command',
                nargs = '*')

        return p


    args = build_parser().parse_args()

    try:
        with open(args.client_id) as fh:
            client_id = fh.readline().strip()
    except Exception:
        client_id = args.client_id

    with open(args.key_file, 'rb') as fh:
        secret = fh.read()

    dp = DigitalPaper(client_id = client_id,
                      key = secret,
                      addr = args.addr)

    #dp.authenticate()

    commands[args.command](dp, *args.command_args)


