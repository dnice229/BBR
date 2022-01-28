# @file config.py
# @func module definitions for framework.
#       Is used to register, define & load modules
#       Starts the main-framework
# @auth Hessel van der Molen
# @date 4 May 2012
# @update 2020 by Arnoud Visser


#dictionairy for module
moduledict = {}
#show frameworks print's (1=show, 0=do not show)
VERBOSE = 1

####
## Register modules:
#######

moduledict["main"]          = "main_v1"
moduledict["globals"]       = [1, "globals"]
moduledict["motion"]        = [1, "motion_v4"]
moduledict["sonar"]         = [1,"sonar_v1"]
moduledict["tools"]         = [1, "tools_v3"]
moduledict["vision"]        = [1, "vision_v2"]
moduledict["behaviour"]     = [1, "behaviour_v1"]

from framework import mframework

###########################
# start & run framework
###########################

if __name__ == '__main__':
     mframework.startUpFramework(moduledict, VERBOSE)
