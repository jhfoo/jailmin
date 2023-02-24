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
    PATH_ARTIFACTS = os.environ['JAILMIN_PATH_ARTIFACTS'] if 'JAILMIN_PATH_ARTIFACTS' in os.environ else '/usr/home/jhfoo/jailmin-artifacts/'

    print (f'Processing in thread: FolderId {self.FolderId}')
    if not os.path.isdir(PATH_ARTIFACTS + self.FolderId):
      return f'Invalid FolderId: {self.FolderId}'

    print (PATH_ARTIFACTS + self.FolderId)

    # sanity check
    DeployFile = f'{PATH_ARTIFACTS}{self.FolderId}/deploy.sh'
    if not os.path.isfile(DeployFile):
      return f'Missing script: deploy.sh'

    VarsFile = f'{PATH_ARTIFACTS}{self.FolderId}/vars.yml'
    with open(DeployFile,'r') as hDeployFile:
      DeployFileContent = hDeployFile.read()

      if os.path.isfile(VarsFile):
        with open(VarsFile,'r') as infile:
          vars = yaml.safe_load(infile)
          for key in vars.keys():
            DeployFileContent = DeployFileContent.replace(f'${key}', vars[key])
        
        print(DeployFileContent)

      TmpDeployFile = f'{PATH_ARTIFACTS}{self.FolderId}/deploy.tmp.sh'  
      with open(TmpDeployFile,'w') as outfile:
        outfile.write(DeployFileContent)

      FileStat = os.stat(TmpDeployFile)
      os.chmod(TmpDeployFile, FileStat.st_mode | stat.S_IEXEC)


    # result = subprocess.run(['ls','-l'], 
    result = subprocess.run(['sudo','./deploy.tmp.sh', self.FolderId], 
      capture_output=True, text=True,
      cwd = PATH_ARTIFACTS + self.FolderId)
    print (result.stdout)
    print (result.stderr)

    print ('Thread end')