{{#stache}}
<li data-id="{{id}}">{{name}}</li>
{{/stache}}

{{^stache}}
{{#.}}
<li data-id="{{attributes.id}}">{{attributes.name}}</li>
{{/.}}
{{/stache}}
