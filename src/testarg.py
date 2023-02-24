# core lib
import argparse
import json
import os
import sys
import uvicorn

# custom lib
import SetupJailEnv
import CmdRestart
import CmdBootstrap
import CmdTemplate
import CmdConsole
import CmdClient
import CmdServer

CMD_CREATE = 'create'
CMD_INIT = 'init'
CMD_RESTART = 'restart'
CMD_CONSOLE = 'console'
CMD_CONSOLE2 = 'con'
CMD_BOOTSTRAP = 'bootstrap'
CMD_CMD ='cmd'
CMD_CLONE = 'clone'
CMD_CONVERT = 'convert'
CMD_TEMPLATE = 'template'
CMD_CLIENT = 'client'
CMD_SERVER = 'server'

CmdChoices = [CMD_CREATE, CMD_INIT, 
  CMD_RESTART, CMD_CONSOLE, 
  CMD_CONSOLE2, CMD_BOOTSTRAP,
  CMD_CMD, CMD_CLONE,
  CMD_CONVERT, CMD_TEMPLATE,
  CMD_CLIENT, CMD_SERVER]

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
    CmdConsole.execCmd(args)
  elif args.cmd == CMD_BOOTSTRAP:
    CmdBootstrap.execCmd(args)
  elif args.cmd == CMD_TEMPLATE:
    CmdTemplate.execCmd(args)
  elif args.cmd == CMD_CLIENT:
    CmdClient.execCmd(args)
  elif args.cmd == CMD_SERVER:
    HOST = os.environ['JAILMIN_SVC_HOST'] if 'JAILMIN_SVC_HOST' in os.environ else '0.0.0.0'
    PORT = os.environ['JAILMIN_SVC_PORT'] if 'JAILMIN_SVC_PORT' in os.environ else 3003

    print (f'Listening on {HOST}:{PORT}')
    # IF statement below must be run in the main script file
    # print ('__name__: ' + __name__)
    if __name__ == '__main__':
      instance = uvicorn.run('server:app', 
        host=HOST,
        port=PORT,
        reload=True)
      print(instance)
    else:
      CmdServer.execCmd(args)
main()

