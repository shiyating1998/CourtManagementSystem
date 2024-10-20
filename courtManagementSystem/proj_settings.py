from decimal import Decimal
from datetime import time

WEEKDAY_PRICES = [
    (time(15, 0), time(18, 0), Decimal('26.00')),
    (time(18, 0), time(22, 0), Decimal('32.00')),
    (time(22, 0), time(23, 0), Decimal('28.00')),
]

WEEKEND_PRICES = [
    (time(7, 0), time(9, 0), Decimal('28.00')),
    (time(9, 0), time(22, 0), Decimal('32.00')),
    (time(22, 0), time(23, 0), Decimal('28.00')),
]

HOLIDAY_PRICE = Decimal('32.00')


VENUE_NAME = "Lions Badminton"
VENUE_STATUS = "Open"

ITEM_NAME = "Badminton"

COURTS = [f"Court {i}" for i in range(1, 11)]
NATURE = 1

TIME_SLOTS = [
    "07:00-08:00",
    "08:00-09:00",
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "12:00-13:00",
    "13:00-14:00",
    "14:00-15:00",
    "15:00-16:00",
    "16:00-17:00",
    "17:00-18:00",
    "18:00-19:00",
    "19:00-20:00",
    "20:00-21:00",
    "21:00-22:00",
    "22:00-23:00",
]

START_HOUR = 7
END_HOUR = 23


