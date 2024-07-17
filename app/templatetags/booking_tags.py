from django import template
from app.models import ItemOrder

register = template.Library()

@register.filter
def split_time_range(time_range):
    start_time, end_time = time_range.split('-')
    return {
        'start_time': start_time.strip(),
        'end_time': end_time.strip(),
    }

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
    for order in item_orders:
        print(order)
    return item_orders


# Store queried items for efficiency
item_orders_cache = None
cached_date = None

#TODO improve efficiency, only query db once
@register.simple_tag
def get_order2(date, start_time, end_time, court):
    global item_orders_cache, cached_date

    if cached_date != date:
        item_orders_cache = list(ItemOrder.objects.filter(date=date))  # Convert queryset to list for easier debugging
        cached_date = date
        print("Queried database for date:", date)
        for order in item_orders_cache:
            print(order)
    matched_orders = [
        order for order in item_orders_cache
        if order.item_time.start_time == start_time
           and order.item_time.end_time == end_time
           and order.item_time.item_court.name == court
    ]

    for order in matched_orders:
        print("Matched order:", order)

    return matched_orders
