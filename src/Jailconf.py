import re

KEY_JAILID = 'JailId'
KEY_DATA = 'data'

class Jailconf:
  def __init__(self, JailId = '', data = {}) -> None:
    self.JailId = JailId
    self.data= data

  def setData(self, key, op = None, value = None):
    value = {
      'op': op,
      'value': value
    }
    self.data[key] = [value]

    return self

  def addData(self, key, op = None, value = None):
    value = {
      'op': op,
      'value': value
    }
    if key in self.data:
      # print ('Appending to key {}'.format(key))
      self.data[key].append(value)
    else:
      self.data[key] = [value]

    return self

  def toFile(self, fname):
    outfile = open(fname, 'w')
    outfile.writelines(self.toString())
    outfile.close()

  def toString(self):
    text = []
    text.append(self.JailId + ' {')
    for key in sorted(self.data.keys()):
      # print ('Array size for {}: {}'.format(key, len(self.data[key])))
      for OpValueCell in self.data[key]:
        OpValue = '' if OpValueCell['op'] == None else ' {} {}'.format(OpValueCell['op'], OpValueCell['value'])
        text.append('  {}{};'.format(key, OpValue))
    text.append('}')

    return '\n'.join(text)

  @classmethod
  def createFromFile(cls, fname):
    STATE_HEADER = 'header'
    STATE_KEYVALUE_PAIRS = 'keyvalue'

    ret = Jailconf()
    infile = open(fname, 'r')
    state = STATE_HEADER
    for line in infile.readlines():
      if state == STATE_HEADER:
        matches = re.search(r'(\S+)\s+{', line)
        if matches:
          ret.JailId = matches.group(1)
          # print ('JailId: {}'.format(ret.JailId))
          state = STATE_KEYVALUE_PAIRS
      elif state == STATE_KEYVALUE_PAIRS:
        matches = re.search(r'}', line)
        if matches:
          return ret
        # else
        matches = re.search(r'\s*(\S+)\s*(\S?=)\s*(.+);', line)
        if matches:
          # print ('To match: {}'.format(line))
          # print ('matches: {}'.format(matches.group(0)))
          key = matches.group(1)
          operator = matches.group(2)
          value = matches.group(3)
          print ('{} => {} => {}'.format(key, operator, value))
          ret.addData(key, operator, value)
        else:
          matches = re.search(r'\s*(\S+);', line)
          if matches:
            key = matches.group(1)
            print ('Operatorless: {}'.format(key))
            ret.addData(key)
          else:
            print ('[WARNING] {}'.format(line))

    return ret
