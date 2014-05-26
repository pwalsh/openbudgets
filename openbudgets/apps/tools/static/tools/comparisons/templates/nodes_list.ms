{{#LatestSheet}}
    {{#attributes}}
    <li data-id="{{id}}" {{#leaf_node}}data-leaf{{/leaf_node}} data-selected="{{selected}}">
        <span class="node_cell node_cell_select"><span class="selectbox"></span></span><span 
        class="node_cell node_cell_type"></span><span
        class="node_cell node_cell_code">{{code}}</span><span
        class="node_cell node_cell_name">{{name}}</span><span
        class="node_cell node_cell_direction">{{direction}}</span>
    </li>
    {{/attributes}}
{{/LatestSheet}}
