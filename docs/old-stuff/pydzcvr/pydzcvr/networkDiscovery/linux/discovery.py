'''


@author:  cboling
@copyright:  2015 organization_name. All rights reserved.
@license:    license
@contact:   user_email
@deffield   updated: Updated
'''

import ns

def _discoverAllLinks(verbose=0):
    # TODO: Local interface discovery here
    
    print 'TODO: Linux Interface: Discover Links'
    
    
def _discoverAllNodes(verbose=0):
    '''
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    
    # TODO: Local interface discovery here    
    print 'TODO: Linux Interface: Discover Nodes'
    
    
    pass

def discover(verbose=0):
    '''
    Discover all nodes and links in the network that are available through 
    Linux network inteface APIs
    
    TODO: This will change radically, for now, just do some hardcoded calls
          to various interfaces and see what is available.  Evenutally this
          will be consolidated once patterns emerge.
    '''
    
    _discoverAllNodes(verbose=verbose)
    _discoverAllLinks(verbose=verbose)
    
    # Look for any linux namespaces for any nodes
    
    ns.discovery.discover(verbose=verbose)
    
    pass