import click
import urllib
import urllib2
import json
import sys
import requests

#base_url = "http://mesosmaster02:8080"
#api_version = "/v2/"
base_url = "http://127.0.0.1:3000"
api_version = "/v1/"

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

	response = urllib2.urlopen(base_url+api_version+"apps")
	data = json.load(response)   
 	for each in data["apps"]:
 		print each["id"][1:]

@marathon.command('kill')
@click.argument('name')
def marathon_killapp(name):
	"""Kills a running app"""
	
	try:
		url = base_url+api_version+"apps/"+name
		r = requests.delete(url)
		
		if r.status_code == 200:
			print "Delete app %s succesful" % name
		else:
			print "Cannot delete app %s" % name 

	except requests.exceptions.RequestException as e:
		print "HTTP error: "+str(e.code)+" "+e.reason 

	except:
		print "Unexpected error:",sys.exc_info()[0]  
		raise

@marathon.command('start')
@click.argument('filename')
def marathon_startapp(filename):
	"""Start a app. Reads input from jsonfile."""
	try:
		file_data = open(filename)
		url =  base_url+api_version+"apps" 
		payload = json.load(file_data)
		headers = {'content-type':'application/json'}
		r = requests.post(url,data=json.dumps(payload),headers=headers)

		# req = urllib2.Request(url)
		#req.add_header('Content-Type', 'application/json')
		#response = urllib2.urlopen(req,json.dumps(data))

	except requests.exceptions.RequestException as e:
		print "HTTP error: "+str(e.code)+" "+e.reason 

	except:
		print "Unexpected error:",sys.exc_info()[0]  
		raise

@marathon.command('changeEnv')
@click.argument('name')
@click.argument('filename')
def marathon_startapp(filename):
	"""Change settings of an app. Read changes from a jsonfile."""
 
	try:
		url = base_url+api_version+"apps/"+name
		file_data = open(filename)
		payload = json.load(file_data)
		headers = {'content-type':'application/json'}
		r = requests.put(url,data=json.dumps(payload),headers=headers)

	except requests.exceptions.RequestException as e:
		print "HTTP error: "+str(e.code)+" "+e.reason 

	except:
		print "Unexpected error:",sys.exc_info()[0]  
		raise
