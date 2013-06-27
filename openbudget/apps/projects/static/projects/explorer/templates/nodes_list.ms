{{#.}}
{{#attributes}}
<li data-id="{{id}}" {{#leaf_node}}data-leaf{{/leaf_node}} data-selected="{{selected}}">
    <span class="selectbox"></span><span 
    class="node_cell node_cell_code">{{code}}</span><span
    class="node_cell node_cell_direction">{{direction}}</span><span 
    class="node_cell node_cell_name">{{name}}</span>
</li>
{{/attributes}}
{{/.}}
