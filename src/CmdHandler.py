import CmdUtil
import Bastille

CMD_LIST = 'list'
CMD_LIST2 = 'ls'
CMD_GUESS = 'guess'
CMD_BOOTON = 'booton'
CND_BOOTOFF = 'bootoff'

def bootJail(args):
  print (args)
  RcConf = CmdUtil.readRcConf()

  # assume BOOTOFF: remove jails in rc.conf that match jails in argument
  RcConfJails = []
  for JailId in RcConf['list']:
    if JailId not in args.JailIds:
      RcConfJails.append(JailId)

  # if BOOTON: append jails to boot string
  if args.cmd == CMD_BOOTON:
    RcConfJails = RcConfJails + args.JailIds

  # update rc.conf
  CmdUtil.setRcConf('bastille_list', ' '.join(RcConfJails))

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

def registerParsers(subparser):
  # reference subparser 
  ListParser = subparser.add_parser(CMD_LIST, aliases=[CMD_LIST2], help='List managed jails')
  ListParser.add_argument('-run', action='store_true')
  ListParser.add_argument('-json','-js', action='store_true')
  ListParser.set_defaults(func=listJails)

  GuessParser = subparser.add_parser(CMD_GUESS, aliases=[], help='Guess jail name')
  GuessParser.add_argument('JailPart')
  GuessParser.set_defaults(func=guessJail)

  BootParser = subparser.add_parser(CMD_BOOTON, aliases=[CND_BOOTOFF], help='Start jail at boot')
  BootParser.add_argument('JailIds', nargs='+')
  BootParser.add_argument('-pos', '-p')
  BootParser.set_defaults(func=bootJail)
