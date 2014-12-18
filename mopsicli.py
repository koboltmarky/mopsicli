import click
import json
import sys
import requests
from termcolor import colored
from marathon.models import MarathonApp
from marathon.models.container import MarathonContainer
from marathon.models.container import MarathonDockerContainer
from marathon.models.container import MarathonContainerPortMapping
from marathon import MarathonClient

BASEURL = 'http://127.0.0.1:3000'
APIVERSION = '/v1/'
#DOCKERURL = 'http://mesosmaster02:4243/'
DOCKERURL = 'http://127.0.0.1:3000/'

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
@click.argument('cmd',required=False)
@click.option('--instances',default=1,help='number of instances')
@click.option('--mem',default=64,help='memory to use')
@click.option('--cpus',default=0.5,help='cpus to use')
@click.option('--ports',default='0,0,0',help='ports the app is listen to.Sytnaxt: port1,port2 or port1:hostport1:serviceport1,port2:hostport2:serviceport2')
def marathon_startapp(image,instances,mem,cpus,cmd,id,ports):
	"""Start a app."""
	
	try:
		url =  BASEURL+APIVERSION+'apps' 
		portsPairList = ports.split(',')
		portsMappingList = []
		for portPair in portsPairList:
			tmpPortList = portPair.split(':')
			container_port = tmpPortList[0]
			try:
				host_port = tmpPortList[1]	
				service_port = tmpPortList[2]
			except IndexError:
				host_port =	0
				service_port = 0
			
			portmapping = MarathonContainerPortMapping(container_port=container_port,host_port=host_port,service_port=service_port,protocol='tcp')
			portsMappingList.append(portmapping)
		
		dockerContainer = MarathonDockerContainer(image,'BRIDGE',portsMappingList)
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
@click.option('--env',help='change the environment variable of a docker container.\nExample: --env \'{"testurl":"test"}\'')
@click.option('--cmd',help='change the cmd param')
def marathon_changeapp(id,env,cmd):
	"""Change settings of an app.Change the env variable."""
  
	try:
		c = MarathonClient('')
		r = requests.get(BASEURL+APIVERSION+'apps/'+id)
		app = c._parse_response(r, MarathonApp, resource_name='app')
		url = BASEURL+APIVERSION+'apps/'+id
		
		if env:
			backup = {}
			backup.update(app.env)
			backup.update(json.loads(env))
			app = MarathonApp(id=id);
			app.env = backup
		else:
			app = MarathonApp(id=id);
		
		if cmd:
			app.cmd = cmd
		
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
def marathon_scaleapp(id,count):
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

@cli.group()
def docker():
	"""Docker commands"""

@docker.command('listContainers')
def docker_listContainer():
	"""List containers"""

	try:
		r = requests.get(DOCKERURL+'containers/json')
		data = r.json()  
		#print data
		print json.dumps(data,indent=4) 
	
	except requests.exceptions.RequestException as e:
		print 'HTTP error: ', e 

	except:
		print 'Unexpected error:', sys.exc_info()[0]  
		raise

@docker.command('tail')
@click.argument('id')
def docker_tail(id):
	"""Tail stdout of a container"""
	try:
		r = requests.get(DOCKERURL+'containers/'+ id +'/logs?stderr=1&stdout=1&timestamps=1&follow=1&tail=10',stream=True)
		print r.headers
		for line in r.iter_lines(chunk_size=10):
			if line:
				print line

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
