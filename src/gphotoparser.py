#/usr/bin/python
# -*- coding: utf-8 -*-
import re
depth= 0

def displaylevel(level):
    global depth
    depth = depth + 1
    if isinstance(level, dict):
        keys = level.keys()
        keys.sort()
        for k in keys:
            if isinstance(level[k],dict):
                print " "*depth,"+",k
                displaylevel(level[k])
            else:
                print " "*depth,"`",k,":",level[k]
    else:
        print " "*depth,"`",level
    depth = depth - 1
        
def parseParams(inputstream):
    tree={}
    current_level = tree
    for line in inputstream:
        if line.startswith('/'):
            hier = line[1:-1].split('/')
            current_level = tree
            for level in hier:
                try:
                    if not current_level.has_key(level):
                        if level == hier[-1]:
                            current_level[level] = {'label':"",'type':"",'choices':{},'current':""}
                        else:
                            current_level[level]={}
                    current_level = current_level[level]
                except:
                    print "erreur avec ",hier
        else:
            label = re.match(r'^\s*Label:\s(.*)$',line)
            if label:
                current_level['label']=label.group(1)
            else:
                choice = re.match(r'^\s*Choice:\s(\d+)\s(.*)$',line)
                if choice:
                    current_level['choices'][choice.group(1)]=choice.group(2)
                else:
                    current = re.match(r'^\s*Current:\s(.*)$',line)
                    if current:
                        current_level['current']=current.group(1)
                    else:
                        ptype = re.match(r'^\s*Type:\s(.*)$',line)
                        if ptype:
                            current_level['type']=ptype.group(1)
    return tree

def extractSubsections(tree):
    subsections = {}
    actioncount = 0
    for section in tree:
        actioncount = actioncount + len(tree[section])
        subsections[section]=tree[section].keys()
    return (actioncount,subsections)
if __name__ == '__main__':
    f = open('eos.txt')
    tree = parseParams(f)
    f.close()
    #displaylevel(tree)

    actioncount,subsections = extractSubsections(tree)



    #print "input : ",len(subsections)," actions : ",actioncount
    #print subsections
    
