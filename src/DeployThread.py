import os
import stat
import subprocess
import threading
import yaml

class DeployThread (threading.Thread):
  def __init__(self, FolderId):
    threading.Thread.__init__(self)
    self.FolderId = FolderId

  def run(self):
    PATH_BASE_ARTIFACTS = os.environ['JAILMIN_PATH_ARTIFACTS'] if 'JAILMIN_PATH_ARTIFACTS' in os.environ else '/usr/home/jhfoo/jailmin-artifacts/'

    print (f'Processing in thread: FolderId {self.FolderId}')
    if not os.path.isdir(PATH_BASE_ARTIFACTS + self.FolderId):
      return f'Invalid FolderId: {self.FolderId}'

    print (PATH_BASE_ARTIFACTS + self.FolderId)
    PATH_ARTIFACTS = f'{PATH_BASE_ARTIFACTS}{self.FolderId}/'

    # sanity check
    DeployFile = f'{PATH_ARTIFACTS}deploy.sh'
    if not os.path.isfile(DeployFile):
      return f'Missing script: deploy.sh'

    VarsFile = f'{PATH_ARTIFACTS}vars.yml'
    with open(DeployFile,'r') as hDeployFile:
      DeployFileContent = hDeployFile.read()

      if os.path.isfile(VarsFile):
        with open(VarsFile,'r') as infile:
          vars = yaml.safe_load(infile)
          # dynamically injected variables
          vars['PathArtifacts'] = PATH_ARTIFACTS

          # global search-replace
          for key in vars.keys():
            # variable can be $MyVarName or ${MyVarName}. The latter for cosmetic reasons
            DeployFileContent = DeployFileContent.replace(f'${key}', vars[key])
            DeployFileContent = DeployFileContent.replace('${'+ key + '}', vars[key])
        
        print(DeployFileContent)

      TmpDeployFile = f'{PATH_ARTIFACTS}deploy.tmp.sh'  
      with open(TmpDeployFile,'w') as outfile:
        outfile.write(DeployFileContent)

      FileStat = os.stat(TmpDeployFile)
      os.chmod(TmpDeployFile, FileStat.st_mode | stat.S_IEXEC)


    # result = subprocess.run(['ls','-l'], 
    # option 1: no live output
    # result = subprocess.run(['sudo','./deploy.tmp.sh', self.FolderId], 
    #   capture_output=True, text=True,
    #   cwd = PATH_ARTIFACTS + self.FolderId)
    # print (result.stdout)
    # print (result.stderr)

    # option 2: live output
    child = subprocess.Popen(['sudo','./deploy.tmp.sh', self.FolderId],
      cwd = PATH_ARTIFACTS,
      shell=False,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      universal_newlines=True)
    while child.poll() is None:
      line = child.stdout.readline().strip()
      if line == '':
        continue
      print (line)

    print ('Thread end')