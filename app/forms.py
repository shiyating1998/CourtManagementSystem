# app/forms.py
from django import forms

class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    selected_slots = forms.CharField(widget=forms.HiddenInput())
