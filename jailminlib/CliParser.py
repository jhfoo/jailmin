# core
import logging
import os
import pathlib
import sys
import json

# public modules
import yaml
# from lib.jailmin import CurrentJailState

# custom modules
import jailminlib.util as util
import jailminlib.statebuilder as statebuilder
import jailminlib.logger as logger
import jailminlib.BastilleFileParser as BastilleFileParser

CLI_CMD_STATE = 'state'
CLI_CMD_TEMPLATE = 'template'
CLI_CMDLIST = [CLI_CMD_STATE, 'build']
CLI_OPTIONS = [{
  'option': '-o',
  'description': '[state] Output file'
}, {
  'option': '-f',
  'description': '[build] Input file'
}]

PATH_BASE = '/usr/local/bastille'

def parseCli():
  if len(sys.argv) < 2:
    print ('USAGE: jailmin {} [options]'.format('|'.join(CLI_CMDLIST)))
    for option in CLI_OPTIONS:
      print ('  {}   {}'.format(option['option'], option['description']))

  ret = {
    'cmd': [],
    'options': {}
  }
  # iterate arguments
  idx = 1
  while idx < len(sys.argv):
    value = sys.argv[idx]
    if idx == 1:
      ret['cmd'].append(value)
    else:
      if value.startswith('--'):
        # parse as key-only option
        ret['options'][value] = True
                
      elif value.startswith('-'):
        # parse as key-value option
        if len(sys.argv) < idx + 1 :
          raise Exception('Missing parameter after {}'.format(value))

        value2 = sys.argv[idx+1]
        ret['options'][value] = value2
        # jump 2 indexes
        idx += 1

      else:
        # parse as commandlet
        ret['cmd'].append(value)
    idx += 1

  if '--dev' in ret['options']:
    logger.info('Logging switched to DEBUG mode')
    logger.setLevel(logging.DEBUG)

  print (ret)
  return ret

def execCmdState(ParsedArgs, JailManager, CurrentJailState):
  if len(ParsedArgs['cmd']) < 2:
    print ('USAGE: jailmin state list|show|priority [--dev|--t]')
    return

  tasks = []
  if ParsedArgs['cmd'][1] in ['list', 'show']:
    print (yaml.dump(CurrentJailState, encoding='utf8').decode('utf-8'))
  elif ParsedArgs['cmd'][1] == 'priority':
    if len(ParsedArgs['cmd']) < 3:
      raise Exception('Missing desired priority level')
    if '-j' not in ParsedArgs['options']:
      raise Exception('Missing JailId')

    JailId = ParsedArgs['options']['-j']
    NewPriority = int(ParsedArgs['cmd'][2])
    tasks = statebuilder.analyzePriorityChange(JailId, CurrentJailState, NewPriority)

  if '--t' in ParsedArgs['options']:
    logger.info('Test mode: no change enacted')
    logger.info ('Tasks to execute:\n{}'.format(json.dumps(tasks, indent=2)))
  else:
    for task in tasks:
      if '--dev' in ParsedArgs['options']:
        logger.debug('task: {}'.format(json.dumps(task, indent=2)))
      JailManager.doTask(task)

def execCmdTemplate(ParsedArgs, JailManager, CurrentJailState):
  try:
    if len(ParsedArgs['cmd']) < 2:
      raise Exception('Complete arguments')

    if not '-j' in ParsedArgs['options']:
      raise Exception ('Missing jail name (-j)')

    # validate template path exists
    TemplateName = ParsedArgs['cmd'][1]
    ParentPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    TemplatePath = PATH_BASE + '/' + TemplateName
    logger.debug('TemplatePath: {}'.format(TemplatePath))
    if not pathlib.Path(TemplatePath).is_dir():
      raise Exception ('Missing template folder: {}'.format(TemplatePath))

    varfile = BastilleFileParser.parseVarfile(ParentPath + '/' + ParsedArgs['options']['-v']) if '-v' in ParsedArgs['options'] else {}

    BastilleFileParser.stageReset()
    BastilleFileParser.stageTemplate(TemplateName, varfile)
    ret = util.execNWait('bastille template {} {}'.format(ParsedArgs['options']['-j'], 'temp/' + TemplateName))


    # validate Bastillefile exists
    # BastilleFile = TemplatePath + '/Bastillefile'
    # if not pathlib.Path(BastilleFile).is_file():
    #   raise Exception ('Missing file: {}'.format(BastilleFile))

    # ExpandedBastilleFile = '\n'.join(BastilleFileParser.parseFile(BastilleFile, ParentPath))

    # # process variables
    # if '-v' in ParsedArgs['options']:
    #   varfile = BastilleFileParser.parseVarfile(ParentPath + '/' + ParsedArgs['options']['-v'])
    #   ExpandedBastilleFile = BastilleFileParser.applyVarfile(ExpandedBastilleFile, varfile)

    # print (ExpandedBastilleFile)

    # # create jail
    # JailName = ParsedArgs['options']['-j']
    # JailRelease = varfile['JAIL_RELEASE']
    # JailInterface = varfile['JAIL_INTERFACE1']
    # JailAddress = '0.0.0.0' if varfile['JAIL_ADDRESS'].lower() == 'dhcp' else varfile['JAIL_ADDRESS']
    # # ExecStdOut = util.execNWait('bastille create -V {} {} {} {}'.format(JailName, JailRelease, JailAddress, JailInterface))
    # # logger.debug (ExecStdOut['output'])

    # # execute template
    # # create random folder
    # os.makedirs('/usr/local/bastille/templates/temp/xxx', exist_ok=True)
    # outfile = open('/usr/local/bastille/templates/temp/xxx/Bastillefile', 'w')
    # outfile.write(ExpandedBastilleFile)
    # outfile.close()
    # ExecStdOut = util.execNWait('bastille template {} {}'.format(JailName, 'temp/xxx'))
    # logger.debug (ExecStdOut['output'])


  except Exception as err:
    print ('ERROR: {}\n'.format(err))
    print ('USAGE: jailmin template <template> -j <jailname> [-v <varfile> | --dev | --t]')

def execCli(ParsedArgs, JailManager, CurrentJailState):
  if len(ParsedArgs['cmd']) == 0:
    # no recognized command parsed
    return 

  if ParsedArgs['cmd'][0] == CLI_CMD_STATE:
    execCmdState(ParsedArgs, JailManager, CurrentJailState)
  elif ParsedArgs['cmd'][0] == CLI_CMD_TEMPLATE:
    execCmdTemplate(ParsedArgs, JailManager, CurrentJailState)
  else:
    print ('Unknown command {}'.format(ParsedArgs['cmd'][0]))
