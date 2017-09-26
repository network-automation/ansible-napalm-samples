import napalm
import sys
import os

def main():


    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver('nxos')

    # Connect:
    device = driver(hostname='192.168.2.3', username='admin',
                    password='Bullf00d')

    print 'Opening ...'
    device.open()

    config_string = """ snmp-server user exampleuser network-admin auth sha testPASS123 """

    device.load_merge_candidate(config=config_string)


    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print '\nDiff:'
    print device.compare_config()

    # You can commit or discard the candidate changes.
    choice = raw_input("\nWould you like to commit these changes? [yN]: ")
    if choice == 'y':
      print 'Committing ...'
      device.commit_config()
    else:
      print 'Discarding ...'
      device.discard_config()

    # close the session with the device.
    device.close()

    print 'Done.'

if __name__ == '__main__':
    main()
