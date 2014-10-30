import click
import urllib
import urllib2
import json
import sys

base_url = "http://mesosmaster02:8080"
api_version = "/v2/"

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
		 query_url = base_url+api_version+"apps/"+name
		 opener = urllib2.build_opener(urllib2.HTTPHandler)
		 req = urllib2.Request(query_url)
		 req.get_method = lambda: 'DELETE' 
		 response = urllib2.urlopen(req) 
		 if response.getcode() == 200:
			 print "Delete app %s succesful" % name
		 else:
			 print "Cannot delete app %s" % name 
   
   except urllib2.HTTPError as e:
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
		 data = json.load(file_data)
		 url =  base_url+api_version+"apps" 
		 req = urllib2.Request(url)
		 req.add_header('Content-Type', 'application/json')
		 response = urllib2.urlopen(req,json.dumps(data))

   except urllib2.HTTPError as e:
       print "HTTP error: "+str(e.code)+" "+e.reason 

   except:
     print "Unexpected error:",sys.exc_info()[0]  
     raise

