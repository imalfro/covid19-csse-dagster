{%- macro surrogate_key(field_list) -%}
    {{ return(adapter.dispatch('generate_surrogate_key', 'dbt_utils')(field_list)) }}
{% endmacro %}

{% macro default__surrogate_key(fields) -%}
    {{ return(dbt_utils.generate_surrogate_key(fields)) }}
{%- endmacro %}