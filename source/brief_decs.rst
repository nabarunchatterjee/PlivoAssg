Brief Description
=================

The program takes a service-name and an action from the user and runs
them on a list of remote servers,names of which are stored in a 
configuration file named 'serv_conf'. 

The usernames and hostnames are read from the configuration file and 
appended to the list env.hosts. Then for each entry in the list it checks
whether the particular host is reachable. If it is reachable the it 'run'-s
the command provided by the user on that remote host. If not then it issues
a warning and moves on to the next host.

The program uses the standard Python modules Fabric,Paramiko and ConfigParser
to achieve the task.

