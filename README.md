# Ansible and NAPALM Samples
This GitHub Repo focuses on comparing [Ansible](https://www.ansible.com/network-automation) and [NAPALM](https://github.com/napalm-automation/napalm) on Cisco NXOS.

## Table of Contents
- [Example 1 - Adding an IP address to an interface](#example-1---adding-an-ip-address-to-an-interface)
- [Example 2 - Backing up a Config](#example-2---backing-up-a-config)

## Example 1 - Adding an IP address to an interface

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

## Example 2 - Backing up a Config

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

NAPALM calls a backup file a *checkpoint* file and can be retrieved using the `_get_checkpoint_file()`.  The code snippet below is only a portion of the code, the whole python file is stored as [get_config.py](get_config.py).

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
