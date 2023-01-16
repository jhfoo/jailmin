# jailmin
Version 2 of the tool to simplify jail management using [Bastille](https://bastillebsd.org/) as the lower-level dependency.

## Goals
- [ ] Improve off-the-shelf Bastille experience 
- [ ] Standardise/automate jail environment creation
- [ ] Simplify jail CRUD actions
- [ ] Make jails distributable

## Requirements
1. Preferably a fresh OS install of the latest release (13.1-RELEASE tested) with ZFS-on-root configured. 
2. Installer (setup.sh) will install required packages.

## Key dependencies
1. [bastille](https://github.com/BastilleBSD/bastille)
2. [Python](https://www.python.org)

## Progress status: 5%
### Notable features
#### Enhanced Bastille commands
Maps Bastille RESTART and CONSOLE commands to smart jail names. E.g. `bastille restart long-jail-name` is replaced with `jailmin restart first-jail-chars`.

Example
```
bastille restart windy-word-jail-name
```
replaced with
```
bastille restart windy
```

If there are ambiguities (windy-word1-jail and windy-word2-jail) the 'smart' jail name needs to be longer to disambiguate (windy-word1).

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
