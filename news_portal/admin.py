from django.contrib import admin
from .models import Ad, News, PortalUser, Reader, ReaderProfile, Reporter, ReporterProfile

# Register your models here.
admin.site.register([Ad, News, Reporter, ReporterProfile, PortalUser, Reader, ReaderProfile])
