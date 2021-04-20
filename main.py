import json
import os

import django
from django.db.models import Q

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "backend.config.settings"
)

django.setup()

from backend.apps.services.models import Locality

with open("locality.json", "r") as f:
    data = json.load(f)

    for local in data:
        if local['district_id']:
            Locality.objects.create(id=local['id'], name=local['name'], district_id=local['district_id'])
        print("Нету id")
    print("ВСЁ")