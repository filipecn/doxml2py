# doxml2py
Converts the xml generated by [Doxygen](http://www.stack.nl/~dimitri/doxygen/) into python objects.

There are several tools on the web that translate Doxygen to other types of documentation structures, like [breathe](https://github.com/michaeljones/breathe), which make a better job than my code. I'm doing doxml2py because all I needed was just a parser that could satisfy my personal needs, it is certainly not complete and you shouldn't trust this code 100%!

All it does is just read the xml and instantiate objects of some classes I created, and that is all, it doesn't generate any documentation or anything else...just objects inside python.

The folder ponos_docs contains the files I use to generate the documentation of my repository Ponos which makes use of doxml2py.

## Usage
First you need to generate a single xml file containing all xmls from Doxygen (remember GENERATE_XML = YES on your Doxyfile to generate the xml files), it can be done using the [xsltproc](http://xmlsoft.org/XSLT/xsltproc2.html) tool:
`xsltproc doc/xml/combine.xslt doc/xml/index.xml > doc/xml/all.xml`

and call ..... to be continued.
