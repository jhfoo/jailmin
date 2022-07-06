# import core
import re

# import custom
import jailminlib.util as util
import jailminlib.logger as logger

class BastilleAdapter:
  def __init__(self) -> None:
      pass

  def getBootOrder(self):
    InFile = open('/etc/rc.conf','r')
    for line in InFile.readlines():
      matches = re.match(r'bastille_list="(.*)"', line)
      if matches != None:
        jails = matches.group(1).split(' ')
        break

    print ('jails: {}'.format(jails))
    InFile.close()

    return jails if len(jails) > 0 else []

  def listJails(self):
    PROPS_SHORTLISTED = ['priority', 'boot']

    result = util.execNWait('bastille list -a', isPrintRealtime=False)
    jails = {}
    for line in result['output'].splitlines():
      matches = re.match(r'\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line)
      if matches != None:
        jail = {
          'id': matches.group(1),
          'state': matches.group(2),
          'ip4': matches.group(3),
          'published': matches.group(4),
          'hostname': matches.group(5),
          'release': matches.group(6),
          'path': matches.group(7),
        }

        if jail['id'] != 'JID':
          jails[jail['id']] = jail

    # parse bastille_list in /etc/rc.conf for
    # autoboot and boot order
    BootOrder = 1
    for JailId in self.getBootOrder():
      if JailId in jails:
        jails[JailId]['BootOrder'] = BootOrder
        BootOrder += 1
      else:
        logger.warning('JailId does not exist: {}'.format(JailId))

    # for jail in ret:
    #   JailProps = self.getJailProperties(jail['id'])
    #   for prop in PROPS_SHORTLISTED:
    #     if prop in JailProps:
    #       jail[prop] = JailProps[prop]

    return list(jails.values())

  def getJailProperties(self, JailId):
    logger.debug ('Reading jail properties for {}'.format(JailId))
    INT_PROPS = ['priority', 'boot']
    result = util.execNWait('bastille get all {}'.format(JailId), isPrintRealtime=False)

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
      logger.info ('bastille set {}={} {}'.format(task['key'], task['value'], task['JailName']))
      util.execNWait('bastille set {}={} {}'.format(task['key'], task['value'], task['JailName']), isPrintRealtime=True)
    else:
      raise Exception('Unknown task (cmd: {})'.format(task['cmd']))