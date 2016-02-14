'''


@author:    Chip Boling
@copyright: 2015 Boling Consulting Solutions. All rights reserved.
@license:   Artistic License 2.0, http://opensource.org/licenses/Artistic-2.0
@contact:   support@bcsw.net
@deffield   updated: Updated
@deffield   updated: Updated
'''

import paramiko
import select
import time

def _remoteCommand(hostname, username, timeout=30, verbose=0):
    
    count = 1
    
    while True:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #client.load_system_host_keys()
            client.connect(hostname, username=username)
        
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % hostname
            return
    
        except:
            print "Could not SSH to %s, waiting for it to start" % hostname
            count += 1
            time.sleep(1)
        
        if count >= timeout:
            print "Could not connect to %s. Giving up" % hostname
            return
         
    # Send the command
    stdin, stdout, stderr = client.exec_command('program')
    
    # Wait for the command to terminate
    while not stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                # Print data from stdout
                print stdout.channel.recv(1024),
        print "stderr: ", stderr.readlines()
        print "stdout: ", stdout.readlines()

    client.close()

def _discoverAllLinks(verbose=0):
    # TODO: Call into any needed APIs
    
    print 'TODO: Linux NS: Discover Nodes links'
    pass
def _discoverAllNodes(verbose=0):
    # TODO: Call into any needed APIs
    
    print 'TODO: Linux NS: Discover Nodes'
    pass

def discover(verbose=0):
    '''
    Discover all nodes in the network that are available through 
    Linux network namespace APIs
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    
    # TODO: Figure out what we need to save and how
    _discoverAllNodes(verbose=verbose)
    _discoverAllLinks(verbose=verbose)
    
    pass