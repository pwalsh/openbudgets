{{#.}}
    <h4>{{ period_start }} - {{ period_end }}: {{ description }}</h4>
    {{#items}}
        <ul id="{{ node.uuid }}" class="clearfix">
            <li class="spreadsheet-col spreadsheet-col-code" data-column="code">{{ node.code }}</li
            ><li class="spreadsheet-col spreadsheet-col-name" data-column="name">{{ node.name }}</li
            ><li class="spreadsheet-col spreadsheet-col-amount" data-column="amount">{{ amount }}</li
            ><li class="spreadsheet-col spreadsheet-col-desc" data-column="description">{{ description }}</li>
        </ul>
    {{/items}}
{{/.}}