from django.db import models
from django.utils import timezone

class Venue(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)  # Assuming status is a string like 'open' or 'closed'
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

class Item(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.venue.name}"

class ItemCourt(models.Model):
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    nature = models.IntegerField()  # Assuming nature is an integer like 1 for indoor, 2 for outdoor
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        nature_str = "Indoor" if self.nature == 1 else "Outdoor" if self.nature == 2 else "Unknown"
        return f"{self.name} ({nature_str}) of {self.item.name}"

class ItemTime(models.Model):
    item_court = models.ForeignKey(ItemCourt, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time} - {self.item_court.name}"

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,null=True,)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # TODO Ensure password is hashed
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Convert first_name and last_name to lowercase before saving
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return (f"{self.username} - {self.first_name} - {self.last_name} "
                f"- {self.email} - {self.phone}")

class ItemOrder(models.Model):
    item_time = models.ForeignKey(ItemTime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    flag = models.IntegerField()  # Assuming 0 for available, 1 for booked, 2 for locked
    date = models.DateField()
    status = models.BooleanField()  # Assuming True for open, False for closed
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        status_str = "Open" if self.status else "Closed"
        return (f"{self.date} - {self.item_time.start_time} - {self.item_time.end_time} -"
                f" {self.user.username if self.user else 'N/A'} - {self.money} -"
                f" {status_str} - {self.item_time.item_court.name}")


# for processing payments (celery)
class ProcessedEvent(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_id