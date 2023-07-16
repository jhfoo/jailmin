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
import CmdUtil
import Bastille

CMD_CREATE = 'create'
CMD_GUESS = 'guess'
CMD_INIT = 'init'
CMD_RESTART = 'restart'
CMD_LIST = 'list'
CMD_LIST2 = 'ls'
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
  CMD_CONVERT, 
  # CMD_TEMPLATE,
  CMD_CLIENT, CMD_SERVER]

def getParsedArgs():
  parser = argparse.ArgumentParser(prog='jailmin', description="Jailmin command line")

  subparser = parser.add_subparsers(dest = 'cmd')

  TemplateParser = subparser.add_parser(CMD_TEMPLATE)
  TemplateParser.add_argument('JailId', help = 'Jail Id')
  TemplateParser.add_argument('TemplatePath', help = 'Template folder')
  TemplateParser.add_argument('-v', dest='vars', nargs=1, help = 'Full path to variables file (YAML format)')

  ConsoleParser = subparser.add_parser(CMD_CONSOLE)
  ConsoleParser.add_argument('JailId', help = 'Jail Id')

  # reference subparser 
  ListParser = subparser.add_parser(CMD_LIST, aliases=[CMD_LIST2], help='List managed jails')
  ListParser.add_argument('-run', action='store_true')
  ListParser.add_argument('-json','-js', action='store_true')
  ListParser.set_defaults(func=listJails)

  GuessParser = subparser.add_parser(CMD_GUESS, aliases=[], help='Guess jail name')
  GuessParser.add_argument('JailPart')
  GuessParser.set_defaults(func=guessJail)


  ServerParser = subparser.add_parser(CMD_SERVER)

  ClientParser = subparser.add_parser(CMD_CLIENT)
  ClientParser.add_argument('artifacts', nargs='*')

  RestartParser = subparser.add_parser(CMD_RESTART)
  RestartParser.add_argument('JailId', help = 'Jail Id')

  # parser.add_argument('cmd', choices = CmdChoices)
  # parser.add_argument('CmdArgs', nargs='*')

  # parser.add_argument('jailname', metavar='jail', type=str, nargs='?', help='jail name')
  # parser.add_argument('-c', '--config', nargs=1)
  # parser.add_argument('-v', '--vars', nargs=1)

  args = parser.parse_args()
  args.func(args)
  return args

  if len(sys.argv) < 2:
    print (parser.print_help())
    sys.exit(0)
  else:
    return parser.parse_args()

def guessJail(args):
  resp = CmdUtil.guessJail(args.JailPart)
  if resp == None:
    print ('No jail matched')
  else:
    print ('Matched jails:')
    if isinstance(resp, str):
      print (f'- {resp}')
    else:
      for id in resp:
        print (f'- {id}')

def listJails(args):
  # print (args)
  jails = Bastille.getAllJails()

  if args.run:
    RunningJails = {}
    JailIds = jails.keys()
    for JailId in JailIds:
      if jails[JailId]['isRunning']:
        RunningJails[JailId] = jails[JailId]
    jails = RunningJails

  if args.json:
    print (jails)
  else:
    print (f'{"Jail Id":20} Is Running')
    print (f'{"-"*20} {"-"*10}')

    JailIds = jails.keys()
    JailIds = sorted(JailIds)
    for JailId in JailIds:
      print (f'{JailId:20} {jails[JailId]["isRunning"]}')

def onTemplate(**kwargs):
  print ('hmm')

def main():
  args = getParsedArgs()
  return

  if args.cmd == CMD_CREATE:
    print (args)
  # elif args.cmd == CMD_LIST or args.cmd == CMD_LIST2:
  #   print (Bastille.getAllJails())
  elif args.cmd == CMD_INIT:
    SetupJailEnv.do()
  elif args.cmd == CMD_RESTART:
    CmdRestart.execCmd(args)
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

