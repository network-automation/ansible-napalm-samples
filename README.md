# Ansible and NAPALM Samples
This GitHub Repo focuses on comparing Ansible NAPALM on Cisco NXOS.

# Example 1 - Adding an IP address to an interface

## Ansible

Ansible has a [nxos_config](http://docs.ansible.com/ansible/latest/nxos_config_module.html) specifically used for making config changes (either entire flat-files) or partials (in this case editing a single interface)
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

To run a playbook use the `ansible-playbook` command:

```
[root@localhost ~]# ansible-playbook ipaddress.yml

PLAY [cisco] *****************************************************************************************************************************************************************************************

TASK [nxos_config] ***********************************************************************************************************************************************************************************
ok: [n9k]

PLAY RECAP *******************************************************************************************************************************************************************************************
n9k                        : ok=1    changed=0    unreachable=0    failed=0
```

# Example 2 - Backing up a Config
