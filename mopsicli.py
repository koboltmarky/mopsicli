import click
import json
import sys
import requests
from termcolor import colored
from marathon.models import MarathonApp
from marathon.models.container import MarathonContainer
from marathon.models.container import MarathonDockerContainer
from marathon import MarathonClient

#BASEURL = 'http://mesosmaster02:8080'
#APIVERSION = '/v2/'
BASEURL = 'http://127.0.0.1:3000'
APIVERSION = '/v1/'

@click.group()
@click.version_option()
def cli():
	"""mopsie cli from mmBash UG"""

@cli.group()
def marathon():
	"""Marathon commands"""

@marathon.command('listapps')
def marathon_listapps():
	"""List running apps"""

	try:
		r = requests.get(BASEURL+APIVERSION+'apps')
		data = r.json()   
		for each in data["apps"]:
			print each["id"][1:]
	
	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('getinfosapp')
@click.argument('name')
@click.option('--fields', nargs=1)
@click.option('--listfields', is_flag=True)
def marathon_getinfoapp(name,fields,listfields):
	"""Get info of a running app"""

	try:
		r = requests.get(BASEURL+APIVERSION+'apps/'+name)
		data = r.json()   
		if listfields:
			try:
				walk(data["app"])	
			except: 
				print 'Unexpected error:',sys.exc_info()[0] 
		elif fields:
			try:
				getKeyValue(data["app"],fields)
			except:
				print 'Value %s not in json array ' % fields				
		else:
			print json.dumps(data,indent=4)
	
	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('kill')
@click.argument('id')
def marathon_killapp(id):
	"""Kills a running app"""
	
	try:
		url = BASEURL+APIVERSION+'apps/'+id
		r = requests.delete(url)
		
		if r.status_code == 200:
			print "Delete app %s succesful" % id
		else:
			print 'Cannot delete app %s' % id

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('start')
@click.argument('id')
@click.argument('image')
@click.argument('cmd')
@click.option('--instances',default=1,help='number of instances')
@click.option('--mem',default=64,help='memory to use')
@click.option('--cpus',default=1,help='cpus to use')
def marathon_startapp(image,instances,mem,cpus,cmd,id):
	"""Start a app."""
	
	try:
		url =  BASEURL+APIVERSION+'apps' 
		dockerContainer = MarathonDockerContainer(image,'BRIDGE',[])
		marathonContainer = MarathonContainer(dockerContainer,'DOCKER',[])
		app = MarathonApp(id=id,cmd=cmd,mem=mem,cpus=cpus,container=marathonContainer,instances=instances)
		payload = app.to_json()
		headers = {'content-type':'application/json'}
		r = requests.post(url,payload,headers=headers)
		print r.text	

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('changeEnv')
@click.argument('id')
@click.option('--env',default= {"URL" : "http://test"},help='change the environment variable of a docker container')
def marathon_changeapp(id,env):
	"""Change settings of an app.Change the docker env variable.Overrides the actually setting."""
 
	try:
		c = MarathonClient('http://localhost:8080')
		r = requests.get(BASEURL+APIVERSION+'apps/'+id)
		app = c._parse_response(r, MarathonApp, resource_name='app')
		url = BASEURL+APIVERSION+'apps/'+id
		backup = {}
		backup.update(app.env)
		backup.update(json.loads(env))
		app = MarathonApp(id=id);
		app.env = backup
		payload = app.to_json()
		headers = {'content-type':'application/json'}
		r = requests.put(url,payload,headers=headers)
		print r.text

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('scale')
@click.argument('id')
@click.argument('count')
def marathon_scaleapp(name,count):
	"""Scale an running app."""
 
	try:
		url = BASEURL+APIVERSION+'apps/'+id
		payload = {"instances" : count }
		headers = {'content-type':'application/json'}
		r = requests.put(url,data=json.dumps(payload),headers=headers)
		print r.text

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ', e 

	except:
		print 'Unexpected error:', sys.exc_info()[0]  
		raise

def walk(node):
	for key,item in node.items():
			if isinstance(item,dict):
				walk(item)
			else: 
				print colored(key,'red'), ':', item	

def getKeyValue(node,searchkey):
	for key,item in node.items():
			if isinstance(item,dict):
				getKeyValue(item,searchkey)
			else: 
				if key == searchkey:
					print colored(key,'red'), ':', item	
