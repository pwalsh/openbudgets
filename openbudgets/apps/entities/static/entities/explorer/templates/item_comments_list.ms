{{#discussion}}
<li class="item_comment" data-id="{{id}}">
    <span class="item_comment_user_avatar" style="background-image:url({{#get_user_avatar}}{{user.avatar}}{{/get_user_avatar}});"></span>
    <span class="item_comment_user_name" data-i18n="by" data-i18n-attr="data-prefix" data-prefix="by">{{user.first_name}} {{user.last_name}}</span>
    <span class="item_comment_date">{{#parse_date}}{{created_on}}{{/parse_date}}</span>
    <p class="item_comment_text">{{#lines_to_brs}}{{comment}}{{/lines_to_brs}}</p>
</li>
{{/discussion}}
