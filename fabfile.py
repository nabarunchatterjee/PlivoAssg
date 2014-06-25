from __future__ import with_statement
from fabric.api import env,run,settings
from ConfigParser import SafeConfigParser
import paramiko
import os


def cli_control(service="/etc/init.d/apache2",action="status"):
	""" Takes a service and a action as input and executes them 
	    on a remote machine"""
	fh = open("failed.log","ab")
	if is_host_up(env.host, int(env.port)) and is_keybased_ssh(env.host_string)  is True:
		with settings(warn_only=True):
				output = run("%s %s"%(service,action),quiet=True)
				print(output+'\n')
			
		if output.failed :
			fh.write('\n\n Failed to execute %s %s on %s port %d \n'%(service,action,env.host_string,int(env.port)))
			fh.write(output)		
	fh.close()		

#This function is a modification of a code at 
#http://stackoverflow.com/questions/1956777/how-to-make-fabric-ignore-offline-hosts-in-the-env-hosts-list
def is_host_up(host,port):
	"""Checks whether a host is reachable""" 
	fh = open("host_down.log","ab")
	host_status = False
	try:
	        transport = paramiko.Transport((host, port))
	        host_status = True
	except:
	        print('***Warning*** Host %s on port %s is down.'%(host,port) + '\n')
	        fh.write('***Warning*** Host %s on port %s is down.'%(host,port) + '\n')
	fh.close()   
	return host_status

def is_keybased_ssh(host):
	"""Checks Authentication Errors"""
	temp = host.partition('@')
	user = temp[0]
	hostname = temp[2]
	host_status = True
	fh = open("authentication_failed.log","ab")
	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname,22,user)
		
	except paramiko.AuthenticationException, e:
		print(str(e))
		fh.write('\n\n%s : '%(host) + str(e))
		host_status = False
		
	fh.close()
	return host_status



def server_config_parse():
	""" Parses a configuration file containing usernames and hosts 
	    and stores them in env.hosts"""
	parser = SafeConfigParser()
	parser.read('serv_conf')
	
	for section_name in parser.sections():
		for name,value in parser.items(section_name):
			if(name == 'username'):
				username = value
			if(name == 'host'):
				host = value
		env.hosts.append('%s@%s'%(username,host))
