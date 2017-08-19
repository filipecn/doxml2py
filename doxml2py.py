#!/usr/bin/python

import sys
from subprocess import call
from subprocess import check_output
import xml.etree.ElementTree as ET
from jinja2 import Template
import re
import importlib

reload(sys)
sys.setdefaultencoding('utf-8')


def getList(node, child, field, value):
    return list(filter(lambda c: c.get(field) == value, node.findall(child)))


def getInstanceList(className, node, child):
    class_ = getattr(importlib.import_module("doxml2py"), className)
    instList = []
    if node is not None:
        instList = [class_(t) for t in node.findall(child)]
    instList = sorted(instList, key=lambda x: x.name)
    return instList


def getOne(node, child, field, value):
    instList = list(
        filter(lambda c: c.get(field) == value, node.findall(child)))
    if len(instList) > 0:
        return instList[0]
    return None


def getText(node, field):
    try:
        t = node.find(field).text
    except:
        t = None
    if t is None:
        return ''
    return t


class Compound:
    def __init__(self, c):
        self.object = c
        try:
            self.fullName = c.find('compoundname').text
            self.name = self.fullName.split('::')[-1]
        except:
            self.fullName = ""
            self.name = ""
        self.kind = c.get('kind')
        self.id = c.get('id')
        self.briefdescription = ""
        self.detaileddescription = ""
        if c.find('briefdescription').find('para') is not None:
            self.briefdescription = c.find('briefdescription').find(
                'para').text
        if c.find('detaileddescription').find('para') is not None:
            self.detaileddescription = \
                c.find('detaileddescription').find('para').text


class Param:
    def __init__(self, m, p):
        self.type = getText(p, 'type')
        self.name = getText(p, 'declname')
        self.defval = getText(p, 'defval')
        self.detaileddescription = ""
        try:
            paramList = getOne(
                m.find('detaileddescription').find('para'), 'parameterlist',
                'kind', 'param')
            if paramList is not None:
                pList = paramList.findall('parameteritem')
                for pl in pList:
                    if pl.find('parameternamelist')\
                            .find('parametername').text == self.name:
                        self.detaileddescription = \
                            pl.find('parameterdescription').find('para').text
        except:
            pass


class Method(Compound):
    def __init__(self, m):
        Compound.__init__(self, m)
        self.name = getText(m, 'name')
        self.object = m
        self.definition = getText(m, 'definition')
        self.args = getText(m, 'argsstring')
        self.type = getText(m, 'type')
        self.params = [Param(m, p) for p in m.findall('param')]
        self.returnDescription = ''
        try:
            if self.type is not None and self.type != 'void'\
                    and self.type != '':
                self.returnDescription = m.find('detaileddescription') \
                    .find('para').find('simplesect').find('para').text
        except:
            pass


class Class(Compound):
    def __init__(self, cl):
        Compound.__init__(self, cl)
        self.includes = getText(cl, 'includes')
        self.fields = getList(cl, 'sectiondef', 'kind', 'public-attribute')
        methodList = getOne(cl, 'sectiondef', 'kind', 'public-func')
        self.methods = getInstanceList('Method', methodList, 'memberdef')
        templates = cl.find('templateparamlist')
        self.templateParameters = []
        if templates is not None:
            self.templateParameters =\
                [Param(templates, p) for p in templates.findall('param')]


class Group(Compound):
    def __init__(self, g):
        Compound.__init__(self, g)


class Namespace(Compound):
    def __init__(self, n, classList):
        Compound.__init__(self, n)
        self.classes = [
            list(filter(lambda c: c.id == cl.get('refid'), classList))[0]
            for cl in n.findall('innerclass')
        ]
        self.classes = sorted(self.classes, key=lambda x: x.name)
        functionList = getOne(n, 'sectiondef', 'kind', 'func')
        self.functions = getInstanceList('Method', functionList, 'memberdef')


class Typedef(Compound):
    def __init__(self, t):
        Compound.__init__(self, t)
        self.name = t.find('name').text
        self.definition = t.find('definition').text


class File(Compound):
    def __init__(self, f):
        Compound.__init__(self, f)
        typedefList = getOne(f, 'sectiondef', 'kind', 'typedef')
        self.typedefs = getInstanceList('Typedef', typedefList, 'memberdef')


class ConvertedData:
    def __init__(self):
        self.classes = []


def cleanName(n):
    return n.replace("::", "").replace("<", "").replace(">", "").replace(
        ",", "").replace(" ", "")


def doxml2py(xml_file, data):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    groups = [
        Group(gp)
        for gp in list(
            filter(lambda child: child.get('kind') == 'group', root))
    ]
    groups = sorted(groups, key=lambda x: x.name)
    data.classes = [
        Class(cl)
        for cl in list(
            filter(
                lambda child: child.get('kind') == 'class' or child.get('kind') == 'struct' or child.get('kind') == 'union',
                root))
    ]
    data.classes = sorted(data.classes, key=lambda x: x.name)
    files = [
        File(f)
        for f in list(filter(lambda child: child.get('kind') == 'file', root))
    ]
    files = sorted(files, key=lambda x: x.name)
    namespaces = [
        Namespace(n, data.classes)
        for n in list(
            filter(lambda child: child.get('kind') == 'namespace', root))
    ]
    namespaces = sorted(namespaces, key=lambda x: x.name)
