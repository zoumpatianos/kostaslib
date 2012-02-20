#!/usr/bin/python
"""
@author: Kostas Zoumpatianos
@description: Task automator
"""

import getopt, sys
from time import gmtime, strftime
from terminal import render

class Automator(object):
    current_runlevel = 0

    @classmethod
    def action(self,  foo):
        def magic( self , action) :
            print render('%(BOLD)s%(BG_YELLOW)s%(BLACK)s ' +
                         str(self.current_runlevel) +
                         ' %(NORMAL)s%(BOLD)s%(YELLOW)s%(BG_BLACK)s ' + 
                         strftime("%Y-%m-%d %H:%M:%S", gmtime()) + 
                         ' %(NORMAL)s%(BG_GREEN)s%(WHITE)s%(BOLD)s ' + foo.__name__ + 
                         ' %(NORMAL)s%(BOLD)s%(BLACK)s%(BG_WHITE)s ' + action['description'] +
                         ' %(NORMAL)s')
            
            print render("%(BG_BLACK)s%(BLUE)s")
            result = foo( self )
            print render("%(NORMAL)s")
            return result
            #print "\033[1;m"
                        
            #print "[%s \033[1;32m Action %s finished\033[1;m]" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), foo.__name__)
            
        return magic

    def initialize():
        self.actions = []
        self.parameters = []


    def parse_parameters(self, argv):        
        try:
            opts, args = getopt.getopt(sys.argv[1:], "",
                                       map(lambda x: x+"=", self.parameters))
        except getopt.GetoptError, err:
            print str(err) 
            #usage()
            sys.exit(2)

        for o, a in opts:
            self.parameters[o[2:]]["value"] = a
        

    def value_of(self, parameter):
        return self.parameters[parameter]["value"]

    def name_of(self, parameter):
        return self.parameters[parameter]["name"]

    def __init__(self, argv):
        self.initialize()
        self.parameters["runlevel"] = {"value":0 , "name": "Run level"}
        self.parameters["stopat"] = {"value":len(self.actions), "name": "Stop at"}
        self.parse_parameters(argv)

        if not str(self.value_of("stopat")).isdigit():
            self.parameters["stopat"] = {"value": int(self.get_runlevel_of(self.value_of("stopat"))), 
                                         "name": "Stop at"}
        
        if str(self.value_of("runlevel")).isdigit():
            self.start(self.value_of("runlevel"))
        else:
            runlevel = self.get_runlevel_of(self.value_of("runlevel"))
            self.start(runlevel)
    
        print render('%(RED)s%(BOLD)sFinished!%(NORMAL)s')
        
        
    def start(self, runlevel=0):
        self.current_runlevel = int(runlevel)
        for action in self.actions[int(runlevel):int(self.value_of("stopat"))+1]:
            action_succeeded = action["action"](action)
            if not action_succeeded:
                break
            self.current_runlevel += 1
            

        self.current_runlevel = 0

    def get_runlevel_of(self,action_name):
        for index, action in enumerate(self.actions):
            if action['name'] == action_name:
                return index


