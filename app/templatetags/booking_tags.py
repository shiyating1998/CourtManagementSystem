from django import template
from app.models import ItemOrder
from datetime import datetime, date, timedelta, time

register = template.Library()

@register.filter
def compare_times(start_time, current_time):
    return start_time[:2] <= current_time[11:]

@register.filter
def split_time_range(time_range):
    start_time, end_time = time_range.split('-')
    return {
        'start_time': start_time.strip(),
        'end_time': end_time.strip(),
    }

#TODO what's a good way to improve efficiency
# instead of querying db every single time?
@register.simple_tag
def get_order(date, start_time, end_time, court):
    # print("date:", date)
    # print("start_time:", start_time)
    # print("end_time:", end_time)
    # print("court:", court)

    item_orders = ItemOrder.objects.filter(
        date=date,
        item_time__start_time=start_time,
        item_time__end_time=end_time,
        item_time__item_court__name=court
    )
    #for order in item_orders:
        # print(order)
    return item_orders

