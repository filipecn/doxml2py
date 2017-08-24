---
title: {{ namespace.kind }} {{ namespace.name }}
name: {{ namespace.name }}
position: {{ pos }}
type:
searchPath: {{ searchPath }}
description:
right_code: |
  <div class="code-viewer"><div class="language-bash highlighter-rouge" style="display: block;"><pre class="highlight">
{{ tree }}  </pre></div></div>
---
{% if namespace.classes[0] is defined %}
|Class|Description|
|-----|-----------|
{% for c in namespace.classes: %}|[{{c.name.split("::")[1]}}](/{{ namespace.name }}/{{ c.name.split("::")[1] }})|{{c.briefdescription}}|
{% endfor %}
{% endif %}
#### Typedefs
~~~ cpp
{% for f in fs: %}{% for t in f.typedefs: %}{{t.definition}}
{% endfor %}{% endfor %}~~~
{% if namespace.functions[0] is defined %}
#### Functions
<div class="code-viewer"><div class="language-bash highlighter-rouge" style="display: block;"><pre class="highlight">
{% for f in namespace.functions: %}{{ f.definition }} {{ f.args }}
{% endfor %}</pre></div></div>
{% endif %}

