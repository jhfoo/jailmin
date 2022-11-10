# core lib
import ipaddress
import re
import subprocess
import sys

# public lib
import psutil

# custom lib
from Jailconf import Jailconf

DEF_DHCP_START_BUFFER = 20
DEF_DHCP_END_BUFFER = 55
DEF_BASE_IMAGE = '13.1-RELEASE'
DEF_BRIDGE_NAME = 'public'


def getOptionInput(text, default = None, IsYesNo = True, IsYesDefault = False, IsNoDefault = False, choices = None):
  if default == None:
    if IsYesNo:
      if IsYesDefault:
        OptionStr = 'Y/n'
      elif IsNoDefault:
        OptionStr = 'y/N'
      else:
        OptionStr = ''
  else:
    OptionStr = default

  while True:
    resp = input (text + ' [{}]'.format(OptionStr)).lower()
    if resp == '':
      # no selection: use default if set
      if IsYesDefault:
        resp = 'y'
        break
      elif IsNoDefault:
        resp = 'n'
        break
      elif not default == '':
        resp = default
        break
    else:
      # custom input
      # must choose from list
      if not choices == None:
        if resp in choices:
          return resp
        else:
          print ('Options: {}'.format(choices))
      elif default != None:
        return resp
      elif IsYesNo:
        if resp == 'y' or resp == 'n':
          break
      else:
        break

  return resp

def execShell(cmd):
  proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
  while True:
    line = proc.stdout.readline()
    print (line.strip())
    PollResult = proc.poll()
    # print (PollResult)
    if line == '' and PollResult is not None:
      break

def updatePfConf(BridgeSubnet, InternetInterface):
  infile = open('/etc/pf.conf', 'r')
  lines = [
    '# JAILMIN START: do not edit',
    'WANIF = "{}"'.format(InternetInterface),
    'JAILNET = "{}"'.format(BridgeSubnet),
    'nat on $WANIF inet from { $JAILNET } to any -> {$WANIF}',
    '# JAILMIN END: do not edit',
  ]

  isSkipLine = False
  for line in infile.readlines():
    if re.search('# JAILMIN START', line):
      isSkipLine = True
    elif re.search('# JAILMIN END', line):
      isSkipLine = False
    elif not isSkipLine:    
      lines.append(line.strip())
  infile.close()

  outfile = open('/etc/pf.conf','w')
  for line in lines:
    outfile.write(line + '\n')
  outfile.close()

  execShell('pfctl -f /etc/pf.conf')

def do():
  # conf = Jailconf.createFromFile('/usr/local/bastille/jails/dhcpsvc/jail.conf')
  # print (conf.toString())
  # conf.toFile('/usr/local/bastille/jails/dhcpsvc/jail.conf')
  # sys.exit(0)

  print ('Interfaces: ', end='')
  interfaces = []
  for intf in psutil.net_if_addrs().keys():
    if not intf == 'lo0':
      interfaces.append(intf)

  print ('OK')
  for intf in interfaces:
    print ('- {}'.format(intf))

  # get custom params
  BridgeSubnet = ipaddress.ip_network(getOptionInput('- Bridge subnet?', default='192.168.100.0/24'))
  BridgeIp = next(BridgeSubnet.hosts())
  print ('- Bridge ip is {}/{}'.format(BridgeIp,BridgeSubnet.prefixlen))

  # update rc.conf
  resp = getOptionInput('Update rc.conf?', IsYesDefault=True)
  if resp == 'y':
    execShell('./bin/install-rc.conf {}/{}'.format(BridgeIp, BridgeSubnet.prefixlen))

  # update pf.conf
  resp = getOptionInput('Update pf.conf?', IsYesDefault=True)
  if resp == 'y':
    InternetInterface = getOptionInput('- Internet interface?', default=interfaces[0], choices=interfaces)
    updatePfConf(BridgeSubnet = BridgeSubnet, InternetInterface = InternetInterface)

  # install dhcp jail
  resp = getOptionInput('Install DHCP service?', IsYesDefault=True)
  if resp == 'y':
    DhcpJailIp = BridgeIp + 1
    print ('- DHCP svc addr: {}'.format(DhcpJailIp))
    DefaultDhcpStart = BridgeIp + DEF_DHCP_START_BUFFER
    DhcpStart = getOptionInput('- DHCP start address?', default=DefaultDhcpStart)
    DefaultDhcpEnd = BridgeSubnet.broadcast_address - DEF_DHCP_END_BUFFER
    DhcpEnd = getOptionInput('- DHCP end address?', default=DefaultDhcpEnd)

    JailName = 'dhcpsvc'
    execShell('bastille stop {}'.format(JailName))
    execShell('bastille destroy {}'.format(JailName))
    execShell('bastille create -B {jail} {image} {addr} {interface}'.format(
      jail = JailName,
      image = DEF_BASE_IMAGE,
      addr = DhcpJailIp,
      interface = DEF_BRIDGE_NAME))
    execShell('bastille sysrc {} defaultrouter={}'.format(JailName, BridgeIp))
    execShell('bastille restart {}'.format(JailName))

  # conf = Jailconf.createFromFile('/usr/local/bastille/jails/dhcpsvc/jail.conf')
  # resp = getOptionInput('Restart network?', IsYesDefault=True)
  # if resp == 'y':
  #   execShell('sudo service netif restart')