{{#stache}}
<li data-id="{{node}}" data-item="{{id}}" {{#leaf_item}}data-leaf{{/leaf_item}}>
    <span class="item_cell item_cell_type"></span><span
    class="item_cell item_cell_code">{{code}}</span><span
    class="item_cell item_cell_name">{{name}}</span><span
    class="item_cell item_cell_direction">{{direction}}</span><span
    class="item_cell item_cell_budget amount">{{f_budget}}</span><span
    class="item_cell item_cell_actual amount">{{f_actual}}</span>
</li>
{{/stache}}

{{^stache}}
{{#.}}
{{#attributes}}
<li data-id="{{node}}" data-item="{{id}}" {{#leaf_item}}data-leaf{{/leaf_item}}>
    <span class="item_cell item_cell_type"></span><span
    class="item_cell item_cell_code">{{code}}</span><span
    class="item_cell item_cell_name">{{name}}</span><span
    class="item_cell item_cell_direction">{{direction}}</span><span
    class="item_cell item_cell_budget amount">{{#commas}}{{budget}}{{/commas}}</span><span
    class="item_cell item_cell_actual amount">{{#commas}}{{actual}}{{/commas}}</span>
</li>
{{/attributes}}
{{/.}}
{{/stache}}
