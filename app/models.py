from django.db import models

# TODO
# id = db.Column(db.Integer, primary_key=True)
# first_name = db.Column(db.String(50), nullable=False)
# last_name = db.Column(db.String(50), nullable=False)
# email = db.Column(db.String(120), nullable=False)
# phone = db.Column(db.String(20), nullable=False)

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)  # Assuming status is a string like 'open' or 'closed'

class Item(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

class ItemCourt(models.Model):
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    nature = models.IntegerField()  # Assuming nature is an integer like 1 for indoor, 2 for outdoor

class ItemTime(models.Model):
    item_court = models.ForeignKey(ItemCourt, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  #TODO Ensure password is hashed

class ItemOrder(models.Model):
    item_time = models.ForeignKey(ItemTime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    flag = models.IntegerField()  # Assuming 0 for available, 1 for booked, 2 for locked
    date = models.DateField()
    status = models.BooleanField()  # Assuming True for open, False for closed
