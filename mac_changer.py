#!/usr/bin/env python

import subprocess
import optparse
import re

def change_mac(interface, new_mac):
    '''Changing MAC adress'''
    print("[+] Changing MAC for {} as {}".format(interface, new_mac))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface to change')
    parser.add_option('-m', '--mac', dest='new_mac', help='new MAC adress')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    assert (len(options.new_mac) == 17), 'Too short adress'
    assert (options.new_mac.count(':') == 5), 'Adress should have 5 colons'

    return options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if (mac_search):
        return mac_search.group(0)
    else:
        print("[-] Could not read MAC adress")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC: " + current_mac)
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if (current_mac == get_current_mac(options.interface)):
    print("[+] MAC adress was successfully changed to " + current_mac)
else:
    print("[-] MAC adress did not changed ")
