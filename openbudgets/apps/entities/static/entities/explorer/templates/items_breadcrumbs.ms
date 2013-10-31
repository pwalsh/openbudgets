{{#stache}}
<li data-id="{{node}}">{{name}}</li>
{{/stache}}

{{^stache}}
{{#.}}
<li data-id="{{attributes.node}}">{{attributes.name}}</li>
{{/.}}
{{/stache}}
