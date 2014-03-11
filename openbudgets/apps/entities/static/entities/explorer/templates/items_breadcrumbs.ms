{{#stache}}
<li data-id="{{node}}">{{name}}</li>
{{/stache}}

{{^stache}}
{{#Breadcrumbs}}
<li data-id="{{attributes.node}}">{{attributes.name}}</li>
{{/Breadcrumbs}}
{{/stache}}
