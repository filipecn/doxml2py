---
title: {{ cl.kind }} {{ cl.name }}
name: {{ cl.name }}
position: {{ pos }}
type:
description: {{cl.includes}}
searchPath: {{ searchPath }}
right_code: |
  {{cl.includes}}
---
{{ cl.detaileddescription }}

{% if cl.methods[0] is defined %}
| Methods                        | Descriptions |
--------------------------------|---------------------------------------------|
{% for method in cl.methods %}|{{method.type}}{{method.name}}{{method.args}} | {{method.briefdescription}}|
{% endfor %}
{% endif %}

