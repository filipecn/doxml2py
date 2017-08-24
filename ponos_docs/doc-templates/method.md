---
title: {{method.definition}} {{method.args}}
name: {{method.definition.split("::")[2] or method.definition.split("::")[1]}}
position: {{ pos }}
type:
description: {{ method.briefdescription }}
searchPath: {{ searchPath }}
right_code: |
  ~~~ cpp
    {{method.definition}} {{method.args}}
  ~~~
---
{% if method.params[0] is defined %}{% for p in method.params: %}
{{ p.name }}
: {{ p.detaileddescription or ' ' }}
{% endfor %}{% endif%}
{{ method.detaileddescription or ""}}
{% if method.returnDescription != '' %}
**Return:** {{ method.returnDescription }}
{: .info }
{% endif %}
