{% test no_blank_strings(model, column_name) %}
    select {{ column_name }}
    from {{ model }}
    where trim( coalesce({{ column_name }},'') ) = ''
{% endtest %}