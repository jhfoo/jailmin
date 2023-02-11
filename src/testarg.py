# core lib
import argparse
import json
import sys

# custom lib
import SetupJailEnv
import CmdRestart
import CmdBootstrap

CMD_CREATE = 'create'
CMD_INIT = 'init'
CMD_RESTART = 'restart'
CMD_CONSOLE = 'console'
CMD_CONSOLE2 = 'con'
CMD_BOOTSTRAP = 'bootstrap'
CMD_CMD ='cmd'
CMD_CLONE = 'clone'
CMD_CONVERT = 'convert'
CmdChoices = [CMD_CREATE, CMD_INIT, 
  CMD_RESTART, CMD_CONSOLE, 
  CMD_CONSOLE2, CMD_BOOTSTRAP,
  CMD_CMD, CMD_CLONE,
  CMD_CONVERT]

def getParsedArgs():
  parser = argparse.ArgumentParser(prog='jailmin', description="Jailmin command line")
  parser.add_argument('cmd', choices = CmdChoices)
  parser.add_argument('CmdArgs', nargs='*')
  # parser.add_argument('jailname', metavar='jail', type=str, nargs='?', help='jail name')
  # parser.add_argument('-c', '--config', nargs=1)
  # parser.add_argument('-v', '--vars', nargs=1)

  if len(sys.argv) < 2:
    print (parser.print_help())
    sys.exit(0)
  else:
    return parser.parse_args()



def main():
  args = getParsedArgs()
  if args.cmd == CMD_CREATE:
    print (args)
  elif args.cmd == CMD_INIT:
    SetupJailEnv.do()
  elif args.cmd == CMD_RESTART:
    CmdRestart.cmdRestart(args)
  elif args.cmd == CMD_CONSOLE or args.cmd == CMD_CONSOLE2:
    CmdRestart.cmdConsole(args)
  elif args.cmd == CMD_BOOTSTRAP:
    CmdBootstrap.cmdBootstrap(args)
main()

