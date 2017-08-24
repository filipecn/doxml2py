# Module <!-- {{group.object.get('kind')}} --> `{{group.name}}`

{% if group.name == "Common" %}
    value of variable: {{ group.name }}
{% else %}
    variable is not defined
{% endif %}

 Members                        | Descriptions
--------------------------------|---------------------------------------------
{% for member in members %}
  {{member.kind}} {{ member.name }} | {{member.briefdescription}}
{% endfor %}
