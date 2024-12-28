# Jailmin: the lazy Bastille CLI
Jailmin aspires to be the smart Bastille wrapper, so managing jails over CLI is easier (lazier).

# How does it work?
Jailmin maps to the same Bastille commands.

# Installation
## User only
```sh
# in jailmin/
./bin/install-user
# installs to ~/.local/bin
```

## All users
```sh
# in jailmin/
sudo ./bin/install-user
# installs to /usr/local/bin/
```

# Usage
## Notes
Generally all Bastille commands should work as-is. The jailmin
convenience comes from auto-completing jail names.

For example: if there are only the following jails available (regardless if they are running or not):
- nginx
- mysql

To start nginx simply type
```sh
sudo bastille start ng
# jailmin will expand ng into nginx
```
