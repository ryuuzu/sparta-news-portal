from django.contrib import admin
from .models import Ad, News

# Register your models here.
admin.site.register([Ad, News])
