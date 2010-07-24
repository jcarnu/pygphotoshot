#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
pygphotoshot tries to fill the lack of remote cameras operations using gphoto2

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import subprocess
import shlex
import re
import string
gphoto_options={
    'available':'-a',
    'settings':'--set-config capture=on --list-config',
    'settings_choices':'--get-config "%s"',
    'shoot': '--capture-image-and-download --force-overwrite',
}

def takePhoto():
    shoot_args = shlex.split('gphoto2 %s'%gphoto_options['shoot'])
    shoot_pipe = subprocess.Popen(shoot_args)
    shoot_pipe.wait()
    

def getCameraInfos():
    reChoice = re.compile(r'Choice:\s+(\d+)\s+(.*)$')
    reCurrent = re.compile(r'Current: (.*)$')

    settings_args = shlex.split('gphoto2 %s'%gphoto_options['settings'])
    settings_pipe = subprocess.Popen(settings_args,stdout=subprocess.PIPE)
    line_cnt=0
    settings = {}


    for line in settings_pipe.stdout:
        settings[line[:-1]]={'value':None,'choices':[]}

    all_lines = []
    setkey = settings.keys()
    setkey.sort()
    output = string.join(setkey,' --get-config ')
    print output
    skcount = 0
    #for sk in settings.keys():
    #settings_choices_args = shlex.split('gphoto2 %s'%gphoto_options['settings_choices']%sk)
    settings_choices_args = shlex.split('gphoto2 %s'%output)
    #all_lines.append(sk)
    #   print settings_choices_args
    settings_choices_pipe = subprocess.Popen(settings_choices_args,stdout=subprocess.PIPE)
    for lines in settings_choices_pipe.stdout.readlines():
        if lines.startswith("Label: "):
                #settings[sk]['label']=lines[len('Label: '):-1]
            all_lines.append(setkey[skcount])
            skcount=skcount+1
                #choice = reChoice.match(lines)
            #if choice:
            #    settings[sk]['choices'].append((choice.group(1),choice.group(2)))
            #current = reCurrent.match(lines)
            #if current:
            #    settings[sk]['current']=current.group(1)
        all_lines.append(lines)

    #for s in settings:
    #    print settings[s]['label'],'(%s) current value : %s'%(s,settings[s]['current'])
    #    for o in settings[s]['choices']:
    #        print "\t",o[1]
    
    #return settings
    return all_lines
