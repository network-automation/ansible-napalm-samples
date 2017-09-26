# Ansible and NAPALM Samples
This GitHub Repo focuses on comparing Ansible NAPALM on Cisco NXOS.

## Example 1 - Adding an IP address to an interface

### Ansible

Ansible has a [nxos_config](http://docs.ansible.com/ansible/latest/nxos_config_module.html) specifically used for making config changes (either entire flat-files) or partials (in this case editing a single interface).  
```
- hosts: cisco
  connection: local
  tasks:
    - nxos_config:
        lines:
          - no switchport
          - ip address 172.16.1.1/24
        parents: interface Ethernet1/20
        provider: "{{login_info}}"
```        

To run a playbook use the `ansible-playbook` command.  Although not shown here the output will also have color output (yellow=changed, green=OK, red=failed.).

```
[root@localhost ~]# ansible-playbook ipaddress.yml

PLAY [cisco] ******************************************************************

TASK [nxos_config] ************************************************************
ok: [n9k]

PLAY RECAP ********************************************************************
n9k                        : ok=1    changed=0    unreachable=0    failed=0
```

### NAPALM

This demonstration will show NAPLAM in python only mode (meaning no third party integrations).  The config provided is a snippet, you can view the whole code here: [ipaddress.py](ipaddress.py)

```python
###config snippet, rest of config removed for brevity
driver = napalm.get_network_driver('nxos')
# Connect:
device = driver(hostname='192.168.2.3', username='admin',
                password='Bullf00d')
print 'Opening ...'
device.open()

config_string = """ interface Ethernet1/20
                      no switchport
                      ip address 172.16.1.1/24 """

device.load_merge_candidate(config=config_string)

###config snippet, rest of config removed for brevity

device.commit_config()

device.close()
```

To run the program execute the python program:
```
[root@localhost naplam_examples]# python ipaddress.py
```



# Example 2 - Backing up a Config
