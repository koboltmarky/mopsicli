import click
import urllib
import urllib2
import json

@click.group()
@click.version_option()
def cli():
   """kein ahnung"""

@cli.group()
def marathon():
   """Marathon commands"""

@marathon.command('listapps')
def marathon_listapps():
   """List running apps"""
   response = urllib2.urlopen("http://mesosmaster02:8080/v2/apps")
   data = json.load(response)   
   for each in data["apps"]:
    print each["id"][1:]

@marathon.command('kill')
@click.argument('name')
def marathon_killapp(name):
   """Kills a running app"""
   click.echo('Kill app %s' % name) 

@marathon.command('start')
@click.argument('name')
@click.argument('image')
def marathon_startapp(name,image):
   """Start a app"""
   click.echo('Start app %s with image %s' % (name , image)) 
