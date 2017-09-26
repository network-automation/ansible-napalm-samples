import napalm
import sys
import os
from time import gmtime, strftime

def main():
    """Grab a config for the device."""

    time = strftime("%Y-%m-%d@%H-%M", gmtime())
    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver('nxos')

    # Connect:
    device = driver(hostname='192.168.2.3', username='admin',
                    password='Bullf00d')

    print 'Opening ...'
    device.open()
    nxos_facts = device.get_facts()

    checkpoint = device._get_checkpoint_file()
    #print(checkpoint)

    #create the directory if it does not exist
    if not os.path.exists("backup"):
      os.makedirs("backup")

    f = open("backup/" + nxos_facts['hostname'] + "." + time, 'w')
    f.write(checkpoint)
    f.close
    device.close()

if __name__ == '__main__':
    main()
