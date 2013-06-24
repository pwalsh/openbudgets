{{#.}}
{{#attributes}}
<li data-id="{{id}}" {{#leaf_item}}data-leaf{{/leaf_item}} data-selected="{{selected}}">
    <span class="selectbox"></span><span 
    class="item_cell item_cell_code">{{code}}</span><span
    class="item_cell item_cell_direction">{{direction}}</span><span 
    class="item_cell item_cell_name">{{name}}</span>
</li>
{{/attributes}}
{{/.}}
