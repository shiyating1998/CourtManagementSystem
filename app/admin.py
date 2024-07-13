from django.contrib import admin
from .models import Venue, Item, ItemCourt, ItemTime, User, ItemOrder

admin.site.register(Venue)
admin.site.register(Item)
admin.site.register(ItemCourt)
admin.site.register(ItemTime)
admin.site.register(User)
admin.site.register(ItemOrder)
