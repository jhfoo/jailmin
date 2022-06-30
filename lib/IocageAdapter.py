# import core
import re
import logging

# import custom
import lib.util as util
import lib.logger as logger

class IocageAdapter:
  def __init__(self) -> None:
      pass

  def listJails(self):
    PROPS_SHORTLISTED = ['priority', 'boot']

    result = util.execNWait('iocage list', isPrintRealtime=False)
    ret = []

    for line in result['output'].splitlines():
      matches = re.match(r'\|\s+(\d+)\s+\|\s+(\S+)\s+\|\s+(\S+)\s+\|\s+(\S+)\s+\|\s+(\S+)', line)
      if matches != None:
        jail = {
          'id': int(matches.group(1)),
          'name': matches.group(2),
          'state': matches.group(3),
          'release': matches.group(4),
          'ip4': matches.group(5)
        }
        ret.append(jail)

    for jail in ret:
      JailProps = self.getJailProperties(jail['name'])
      for prop in PROPS_SHORTLISTED:
        if prop in JailProps:
          jail[prop] = JailProps[prop]

    return ret

  def getJailProperties(self, JailId):
    logger.debug ('Reading jail properties for {}'.format(JailId))
    INT_PROPS = ['priority', 'boot']
    result = util.execNWait('iocage get all {}'.format(JailId), isPrintRealtime=False)

    ret = {}
    for line in result['output'].splitlines():
      # print (line)
      matches = re.match(r'(.+?):(.+)', line)
      if matches != None:
        key = matches.group(1)
        value = int(matches.group(2)) if key in INT_PROPS else matches.group(2)
        ret[key] = value

    return ret

  def doTask(self, task):
    if task['cmd'] == 'SetProperty':
      logger.info ('iocage set {}={} {}'.format(task['key'], task['value'], task['JailName']))
      util.execNWait('iocage set {}={} {}'.format(task['key'], task['value'], task['JailName']), isPrintRealtime=True)
    else:
      raise Exception('Unknown task (cmd: {})'.format(task['cmd']))