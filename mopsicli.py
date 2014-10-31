import click
import json
import sys
import requests

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
				print 'App as the following variables: \n'
				for each in data["app"]:
					print each
			except: 
				print 'Unexpected error:',sys.exc_info()[0] 
		elif fields:
			try:
				for each in data["app"]:
					if each == fields:
						print "%s : %s" % (each, data["app"][fields])
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
@click.argument('name')
def marathon_killapp(name):
	"""Kills a running app"""
	
	try:
		url = BASEURL+APIVERSION+'apps/'+name
		r = requests.delete(url)
		
		if r.status_code == 200:
			print "Delete app %s succesful" % name
		else:
			print 'Cannot delete app %s' % name 

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('start')
@click.argument('filename')
def marathon_startapp(filename):
	"""Start a app. Reads input from jsonfile."""
	try:
		fileData = open(filename)
		url =  BASEURL+APIVERSION+'apps' 
		payload = json.load(fileData)
		headers = {'content-type':'application/json'}
		r = requests.post(url,data=json.dumps(payload),headers=headers)

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('changeEnv')
@click.argument('name')
@click.argument('filename')
def marathon_changeapp(name,filename):
	"""Change settings of an app. Read changes from a jsonfile."""
 
	try:
		url = BASEURL+APIVERSION+'apps/'+name
		fileData = open(filename)
		payload = json.load(fileData)
		headers = {'content-type':'application/json'}
		r = requests.put(url,data=json.dumps(payload),headers=headers)

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ',e 

	except:
		print 'Unexpected error:',sys.exc_info()[0]  
		raise

@marathon.command('scale')
@click.argument('name')
@click.argument('count')
def marathon_scaleapp(name,count):
	"""Scale an running app."""
 
	try:
		url = BASEURL+APIVERSION+'apps/'+name
		payload = {"instances" : count }
		headers = {'content-type':'application/json'}
		r = requests.put(url,data=json.dumps(payload),headers=headers)

	except requests.exceptions.RequestException as e:
		print 'HTTP error: ', e 

	except:
		print 'Unexpected error:', sys.exc_info()[0]  
		raise
