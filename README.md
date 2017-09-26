# Ansible and NAPALM Samples
This GitHub Repo focuses on comparing [Ansible](https://www.ansible.com/network-automation) and [NAPALM](https://github.com/napalm-automation/napalm) on Cisco NXOS.

## Table of Contents
- [Example 1 - Backing up a Config](#example-2---backing-up-a-config)
- [Example 2 - Adding an IP address to an interface](#example-1---adding-an-ip-address-to-an-interface)
- [Example 3 - Adding a new VLAN](#example-3---adding-a-new-vlan)
- [Example 4 - Change the SNMP password](#example-4---change-the-snmp-password)
## Example 1 - Backing up a Config

### Ansible

Again Ansible can use the nxos_config module for easy backups.  There is a backup parameter that can just be turned to `yes`.  This playbook is stored as [backup.yml](backup.yml) on this git repo.

```
---
- hosts: cisco
  connection: local
  tasks:
    - nxos_config:
        backup: yes
        provider: "{{login_info}}"
```        

Run the playbook with `ansible-playbook backup.yml`

After running the playbook there will be a timestamped config stored under the directory backup:
```
[root@localhost ~]# ls backup
n9k_config.2017-09-26@10:21:28
```

### NAPALM

NAPALM calls a backup file a *checkpoint* file and can be retrieved using the `_get_checkpoint_file()`.  The code snippet below is only a portion of the code, the  python script is stored in this git repo as [get_config.py](get_config.py).

```python
###config snippet, rest of config removed for brevity
checkpoint = device._get_checkpoint_file()
#print(checkpoint)

#create the directory if it does not exist
if not os.path.exists("backup"):
  os.makedirs("backup")

f = open("backup/" + nxos_facts['hostname'] + "." + time, 'w')
f.write(checkpoint)
f.close
device.close()
###config snippet, rest of config removed for brevity
```

Run the python program with `python backup.py`.  The python program will create a folder:
```
[root@localhost naplam_examples]# ls backup/
switch.2017-09-26@15-11
```

## Example 2 - Adding an IP address to an interface

### Ansible

Ansible has a [nxos_config](http://docs.ansible.com/ansible/latest/nxos_config_module.html) specifically used for making config changes (either entire flat-files) or partials (in this case editing a single interface).  This playbook is stored as [ipaddress.yml](ipaddress.yml) on this git repo.
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

This demonstration will show NAPLAM in python only mode (meaning no third party integrations).  The code snippet below is only a portion of the code, the  python script is stored in this git repo as [ipaddress.py](ipaddress.py)

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

## Example 3 - Adding a new VLAN

### Ansible
In addition to the [nxos_config module](http://docs.ansible.com/ansible/latest/nxos_config_module.html) we can use the [nxos_vlan module](http://docs.ansible.com/ansible/latest/nxos_vlan_module.html) to make this really easy.  This playbook is stored as [add_vlan.yml](add_vlan.yml) on this git repo.
```
---
- hosts: cisco
  connection: local
  tasks:
    - nxos_vlan:
        vlan_id: 10
        name: STORAGE
        provider: "{{login_info}}"
```        
Run the playbook with `ansible-playbook add_vlan.yml`

Check to see if the VLAN is configured with a `show running-config vlan 10`
```
switch# show running-config vlan 10

!Command: show running-config vlan 10
!Time: Tue Sep 19 22:39:40 2017

version 7.0(3)I7(1)
vlan 10
vlan 10
  name STORAGE
```

### NAPALM

## Example 4 - Change the SNMP password
A common maintenance task for network operations teams is to change the SNMP password every so often (e.g. every 90 days).  This can also be automated with Ansible and NAPALM.  

2 NOTES:
- To see available groups on NXOS you can look at `show snmp group`.  The network-admin is commonly used for configuration.
- NXOS has some default password complexities.  From the NXOS box: `password strength check: Password should contain characters from at least three of the following classes: lower case letters, upper case letters, digits and special characters.`

### Ansible
For Ansible there is a [nxos_snmp_user module](http://docs.ansible.com/ansible/latest/nxos_snmp_user_module.html) that is available to use.  The  Ansible playbook demonstrated is stored as [change_snmp_password.yml](change_snmp_password.yml).

```
---
- hosts: cisco
  connection: local
  tasks:
    - nxos_snmp_user:
        user: exampleuser
        group: network-admin
        authentication: sha
        pwd: testPASS123
        provider: "{{login_info}}"
```        
To run the playbook perform a `ansible-playbook change_snmp_password.yml`

On the NXOS switch we can perform a `show run | i snmp` to see the new config:
```
switch# sh run | i snmp
snmp-server user admin network-admin auth md5 0xc1ddb036df145c775510428fe3c6b553 priv 0xc1ddb036df145c775510428fe3c6b553 localizedkey
snmp-server user exampleuser network-admin auth sha 0x7071c014b53743ca568dd2c3fd70005c5e21db5e localizedkey
```

### NAPALM

NAPALM treats everything as a config merge or replace so there is no specific module just for SNMP (for configuring, there is a `get_snmp_information()`).  This is very similar where we can merge a flat-file or string into the existing config.  The code snippet below is only a portion of the code, the  python script is stored in this git repo as [change_snmp_password.py](change_snmp_password.py).

```python
###config snippet, rest of config removed for brevity
driver = napalm.get_network_driver('nxos')
# Connect:
device = driver(hostname='192.168.2.3', username='admin',
                password='Bullf00d')
print 'Opening ...'
device.open()

config_string = """ snmp-server user exampleuser network-admin auth sha testPASS123 """

device.load_merge_candidate(config=config_string)

###config snippet, rest of config removed for brevity

device.commit_config()

device.close()
```

To run the program execute the python program:
```
[root@localhost naplam_examples]# python change_snmp_password.py
```

On the NXOS switch we can perform a `show run | i snmp` to see the new config:
```
switch# sh run | i snmp
snmp-server user admin network-admin auth md5 0xc1ddb036df145c775510428fe3c6b553 priv 0xc1ddb036df145c775510428fe3c6b553 localizedkey
snmp-server user exampleuser network-admin auth sha 0x7071c014b53743ca568dd2c3fd70005c5e21db5e localizedkey
```
