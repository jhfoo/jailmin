# core lib
import argparse
import json
import sys

# public lib
import psutil

CMD_CREATE = 'create'
CMD_INIT = 'init'

def getParsedArgs():
  parser = argparse.ArgumentParser(description="Jailmin command line")
  parser.add_argument('cmd', choices=[CMD_CREATE, CMD_INIT])
  parser.add_argument('jailname', metavar='jail', type=str, nargs='?', help='jail name')
  parser.add_argument('-c', '--config', nargs=1)
  parser.add_argument('-v', '--vars', nargs=1)

  if len(sys.argv) < 2:
    print (parser.print_help())
    sys.exit(0)
  else:
    return parser.parse_args()

def setupJailEnv():
  print ('Interfaces: ', end='')
  interfaces = []
  for intf in psutil.net_if_addrs().keys():
    if not intf == 'lo0':
      interfaces.append(intf)

  print ('OK')
  for intf in interfaces:
    print ('- {}'.format(intf))

def main():
  args = getParsedArgs()
  if args.cmd == CMD_CREATE:
    print (args)
  elif args.cmd == CMD_INIT:
    setupJailEnv()

main()

