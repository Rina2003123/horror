import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Item

items = Item.objects.all()
data = [{"name": item.name, "emailAdress": item.emailAdress, "phoneNumber": float(item.phoneNumber)} for item in items]

with open('items_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data exported to items_data.json")