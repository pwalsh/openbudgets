{{#stache}}
<li data-id="{{node}}" data-item="{{id}}" {{#leaf_item}}data-leaf{{/leaf_item}}>
    <span class="item_cell item_cell_type"></span><span
    class="item_cell item_cell_code">{{code}}</span><span
    class="item_cell item_cell_name">{{name}}</span><span
    class="item_cell item_cell_direction">{{direction}}</span><span
    class="item_cell item_cell_budget amount{{#f_budget_empty}} empty{{/f_budget_empty}}">{{f_budget}}</span><span
    class="item_cell item_cell_actual amount{{#f_actual_empty}} empty{{/f_actual_empty}}">{{f_actual}}</span><span
    class="item_cell item_cell_comment"><span class="td_filler">
        <span class="item_comment_button {{#has_comments}}has_comments{{/has_comments}}">!</span>
    </span></span>
</li>
{{/stache}}

{{^stache}}
{{#LatestSheet}}
    {{#attributes}}
        <li data-id="{{node}}" data-item="{{id}}" {{#leaf_item}}data-leaf{{/leaf_item}}>
            <span class="item_cell item_cell_type"></span><span
            class="item_cell item_cell_code">{{code}}</span><span
            class="item_cell item_cell_name">{{name}}</span><span
            class="item_cell item_cell_direction">{{direction}}</span><span
            class="item_cell item_cell_budget amount{{#is_empty}}{{budget}}{{/is_empty}}">{{#commas}}{{budget}}{{/commas}}</span><span
            class="item_cell item_cell_actual amount{{#is_empty}}{{actual}}{{/is_empty}}">{{#commas}}{{actual}}{{/commas}}</span><span
            class="item_cell item_cell_comment"><span class="td_filler">
                <span class="item_comment_button {{#has_comments}}has_comments{{/has_comments}}">!</span>
            </span></span>
        </li>
    {{/attributes}}
{{/LatestSheet}}
{{/stache}}
