# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "VertexColorMaster",
    "author" : "CGDJay",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "CGDJay"
}


#-------------------------------------------------------
import bpy
import os
import subprocess
import sys

#-------------------------------------------------------

# module registrastion method

import importlib

module_names = (
    "pref",

    "vcm_prop",
    "vcm_menus",
    "vcm_Ops",

    

)

modules = []

for module_name in module_names:
    if module_name in locals():
        modules.append(importlib.reload(locals()[module_name]))
    else:
        modules.append(importlib.import_module("." + module_name, package=__package__))


#-------------------------------------------------------
#REGISTER

def register():
    
    for mod in modules:
        mod.register()

#-------------------------------------------------------
#UNREGISTER   

def unregister():

    for mod in modules:
        mod.unregister()
     
if __name__ == '__main__':
    register()
        
        
