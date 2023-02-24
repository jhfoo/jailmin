import os
import DeployThread
from fastapi import FastAPI

app = FastAPI()

def onSignalUp():
  print ('signal up')

@app.get('/')
def root():
  return 'woohoo!'

@app.get('/api/deploy/{FolderId}')
def DeployFolder(FolderId):
  PATH_ARTIFACTS = os.environ['JAILMIN_PATH_ARTIFACTS'] if 'JAILMIN_PATH_ARTIFACTS' in os.environ else '/usr/home/jhfoo/jailmin-artifacts/'

  if not os.path.isdir(PATH_ARTIFACTS + FolderId):
    return f'Invalid FolderId: {FolderId}'

  ret = {
    'FolderId': FolderId,
    'artifacts': [],
    'run': None,
  }
  for item in os.scandir(PATH_ARTIFACTS + FolderId):
    if item.is_file():
      ret['artifacts'].append( item.name)
      if item.name == 'deploy.sh':
        ret['run'] = item.name

  if ret['run'] is None:
    return f"ERROR: Missing deploy.sh for FolderId {FolderId}"
  
  deploy = DeployThread.DeployThread(FolderId)
  deploy.start()

  return ret