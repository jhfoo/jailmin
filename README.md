# jailmin
Version 2 of the tool to simplify jail management using [Bastille](https://bastillebsd.org/) as the lower-level dependency.

## Goals
- [ ] Standardise/automate jail environment creation
- [ ] Simplify jail CRUD actions
- [ ] Make jails distributable

## Requirements
1. Preferably a fresh OS install of the latest release (13.1-RELEASE tested) with ZFS-on-root configured. 
2. Installer (setup.sh) will install required packages.

## Key dependencies
1. [bastille](https://github.com/BastilleBSD/bastille)
2. [Python](https://www.python.org)

## Progress status: 0%

## Install
1. Before running bootstrap cmd below consider enabling zfs support in `/usr/local/etc/bastille/bastille.conf`:
```
# /usr/local/etc/bastille/bastille.conf
bastille_zfs_enable="YES"                                                
bastille_zfs_zpool="zroot"
```
2. CLI steps:
```
git clone https://github.com/jhfoo/jailmin.git
cd jailmin
./bin/install.sh
sudo bastille bootstrap 13.1-RELEASE
```
