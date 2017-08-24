#!/usr/bin/python

import sys
from subprocess import call
from subprocess import check_output
from jinja2 import Template
import re
sys.path.append("/run/media/filipecn/OS/Projects/doxml2py")
from doxml2py import doxml2py
from doxml2py import ConvertedData

reload(sys)
sys.setdefaultencoding('utf-8')

xml_file = sys.argv[1]
data = ConvertedData()
doxml2py(xml_file, data)

namespaceTemplate = Template(open("doc-templates/namespace.md", "r").read())
classTemplate = Template(open("doc-templates/class.md", "r").read())
methodTemplate = Template(open("doc-templates/method.md", "r").read())

# remove old documentation
call(["rm -r doc-web"], shell=True)
call(["mkdir doc-web"], shell=True)
# create directories and copy data to them
call(["mkdir doc-web/_includes"], shell=True)
call(["mkdir doc-web/_layouts"], shell=True)
call(["cp doc-templates/sidebar.html doc-web/_includes"], shell=True)
call(["cp doc-templates/default.html doc-web/_layouts"], shell=True)
call(["cp doc-templates/index.html doc-web/"], shell=True)
call(["cp -r doc-templates/_introduction doc-web"], shell=True)
call(["cp -r doc-templates/aviator/* doc-web"], shell=True)
# generate jekyll's configuration file
jekyllConfig = open("doc-templates/jekyll_config", "r").read()
jekyllConfig = jekyllConfig + "  namespaces:\n"
jekyllConfig = jekyllConfig + "    title: Namespaces\n"
jekyllConfig = jekyllConfig + "    name: Namespaces\n"
jekyllConfig = jekyllConfig + "    position: 2\n"
# position on the list
k = 3
for n in data.namespaces:
    jekyllConfig = jekyllConfig + "  " + n.name + ":\n"
    jekyllConfig = jekyllConfig + "    title: " + n.name + "\n"
    jekyllConfig = jekyllConfig + "    name: " + n.name + "\n"
    jekyllConfig = jekyllConfig + "    position: " + str(k) + "\n"
    k = k + 1
for c in data.classes:
    jekyllConfig = jekyllConfig + "  " + c.name + ":\n"
    jekyllConfig = jekyllConfig + "    title: " + c.name + "\n"
    jekyllConfig = jekyllConfig + "    position: " + str(k) + "\n"
    jekyllConfig = jekyllConfig + "    name: class " + c.name + "\n"
    k = k + 1
open("doc-web/_config.yml", "w").write(jekyllConfig)
# generate markdowns
for c in data.classes:
    dirName = "doc-web/_" + c.namespace + '_' + c.name
    call(["mkdir " + dirName], shell=True)
    open(dirName + "/documentation.md", "w")\
        .write(classTemplate.render(searchPath=c.namespace + "/" +
                                    c.name, cl=c, pos=0))
    for i in range(len(c.methods)):
        methodPath = re.sub(r"(<[^>]+>)", "", c.methods[i].definition)
        methodPath = methodPath\
            .split(" ")[len(methodPath.split(" ")) - 1].split("::")
        open(dirName + "/" + re.sub(r"(>|\*|\/|\+|\=|<)", "",
                                    c.methods[i].name) + ".md", "w")\
            .write(methodTemplate.render(searchPath=c.namespace +
                                         "/" + c.name,
                                         method=c.methods[i],
                                         pos=i + 1))
# generate htmls (one for each class)
for n in data.namespaces:
    if len(n.fullName.split("::")) > 1:
        continue
    dirName = "doc-web/" + n.name + "/"
    call(["mkdir " + dirName], shell=True)
    for c in n.classes:
        classNameID = c.name
        open(dirName + classNameID + ".html", "w")\
            .write("---\ntitle: " + classNameID + "\npageType: class" +
                   "\nclassName: " + c.name + "\n---\n" +
                   open("doc-templates/class_html", "r").read())

exit(1)
# generate namespaces markdowns
dirName = "doc-web/namespaces/"
call(["mkdir " + dirName], shell=True)
for i in range(len(data.namespaces)):
    print "generating namespace " + data.namespaces[i].name
    if len(data.namespaces[i].name.split("::")) > 1:
        continue
    open(dirName + data.namespaces[i].name + ".md", "w")\
        .write(namespaceTemplate.render(
            searchPath="namespace/" + data.namespaces[i].name,
            namespace=data.namespaces[i], pos=i, fs=data.files,
            tree=re.sub(r"([\w]+\.h)", r'<a href="" >\1</a>',
                        re.sub(r"^([^(\n)]+\n)", r"  \1", check_output(
                            "tree -P *.h --noreport " + data.namespaces[i].name +
                            "/src --dirsfirst", shell=True).replace("\t", " "),
                            flags=re.MULTILINE), flags=re.MULTILINE)))

print "generate namespace html's"
dirName = "doc-web/namespace/"
call(["mkdir " + dirName], shell=True)
for n in data.namespaces:
    # create namespace/name.html
    if len(n.name.split("::")) > 1:
        continue
    open(dirName + n.name + ".html", "w")\
        .write("---\ntitle: " + n.name + "\npageType: namespace" +
               "\nnamespace: " + n.name + "\n---\n" +
               open("doc-templates/namespace_html", "r").read())
    # fill _ponos with markdowns
    call(["mkdir doc-web/_" + n.name], shell=True)
    # namespace md
    open("doc-web/_" + n.name + "/namespace.md", "w")\
        .write(namespaceTemplate.render(
            searchPath="namespace/" + n.name, namespace=n, pos=i, fs=files,
            tree=re.sub(r"([\w]+\.h)", r'<a href="" >\1</a>',
                        re.sub(r"^([^(\n)]+\n)", r"  \1", check_output(
                            "tree -P *.h --noreport " + n.name +
                            "/src --dirsfirst", shell=True).replace("\t", " "),
                            flags=re.MULTILINE), flags=re.MULTILINE)))
    # functions md
    i = 1
    for f in n.functions:
        print "functions " + f.name
        print f.briefdescription
        functionName = re.sub(r"(>|\*|\/|\+|\=|<)", "", f.name)
        open("doc-web/_" + n.name + "/" + functionName + ".md", "w")\
            .write(methodTemplate.render(searchPath="namespace/" + n.name,
                                         method=f, pos=i + 1))
        i = i + 1
