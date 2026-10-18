# File: apps/dashboard/templatetags/dashboard_tags.py
from django import template

register = template.Library()

@register.filter(name='currency_format')
def currency_format(value):
    """
    Định dạng số tiền theo chuẩn Việt Nam với dấu chấm phân cách hàng nghìn.
    Ví dụ: 300000 -> '300.000', 30000 -> '30.000', 5970000 -> '5.970.000'
    """
    if value is None or value == '':
        return '0'
    try:
        val = int(round(float(value)))
        return f"{val:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(value)
