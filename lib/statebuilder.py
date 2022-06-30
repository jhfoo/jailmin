# core
import copy
import json

# import custom
from textwrap import indent
import lib.logger as logger

def getCurrentState(JailManager):
  logger.info('Collecting current jail state')
  jails = JailManager.listJails()
  return jails

def sortKey(item):
  return item['priority']

def analyzePriorityChange(JailId, CurrentJailState, NewPriority):
  ret = []

  # rule: no 2 jails can be set to the same priority
  # algo: 
  # - check if jail already has the priority
  # - check if a jail has the same priority
  # - NO: set jail to priority => DONE
  # - YES: 1. set jail to priority
  # -      2. recurse to set jail with conflicting priority to one down

  # manipulate list data safely via clone
  ClonedJails = copy.deepcopy(CurrentJailState)

  TargetJailList = list(filter(lambda jail: jail['name'] == JailId, ClonedJails))
  if len(TargetJailList) == 0:
    raise Exception ('Jail {} not found'.format('JailId'))

  TargetJail = TargetJailList[0]
  if TargetJail['priority'] == NewPriority:
    # nothing to change
    return ret

  ret.append({
    'JailName': JailId,
    'cmd': 'SetProperty',
    'key': 'priority',
    'value': NewPriority
  })
  ConflictingJails = list(filter(lambda jail: jail['priority'] == NewPriority and jail['name'] != JailId, ClonedJails))
  if len(ConflictingJails) == 0:
    # no conflicts: simple property change
    return ret

  # bit complicated: update jail data in cloned list before recurring
  TargetJail['priority'] = NewPriority
  for jail in ConflictingJails:
    ret = ret + analyzePriorityChange(jail['name'], ClonedJails, NewPriority + 1)

  return ret

# switch to file log


