#!/usr/bin/python

from doxml2py import doxml2py
from doxml2py import ConvertedData

xml_file = '/run/media/filipecn/OS/Projects/Ponos/doc/xml/all.xml'
data = ConvertedData()
doxml2py(xml_file, data)
print('classes list:')
for c in data.classes:
    for tp in c.templateParameters:
        print(tp.type + '\t' + tp.name)
    print(c.name + ' with methods')
    for m in c.methods:
        print('\t' + m.type + '\t' + m.name + '\t' + m.args)
        for p in m.params:
            print('\t\t' + p.type + '\t' + p.name + '\t' + p.defval)
