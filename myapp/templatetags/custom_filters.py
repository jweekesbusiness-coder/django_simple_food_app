from django import template

# Custom template filter to format a decimal value as currency
register = template.Library()
# This filter takes a decimal value and formats it as a currency string, prefixed with a dollar sign.
@register.filter(name='currency')
def currency(value):
    return f"${value}"

@register.filter
def discount(value,percentage):
    return int(value) - (int(value) * (int(percentage)/100))