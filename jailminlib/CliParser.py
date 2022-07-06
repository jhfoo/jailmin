# core
import logging
import sys
import json

# public modules
import yaml
# from lib.jailmin import CurrentJailState

# custom modules
import jailminlib.statebuilder as statebuilder
import jailminlib.logger as logger

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
  if len(ParsedArgs['cmd']) < 4:
    print ('USAGE: jailmin template <template> [-j <jailname> | --dev | --t]')
    return

  return

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
