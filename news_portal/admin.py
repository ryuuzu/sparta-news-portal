from tokenize import Comment
from django.contrib import admin
from .models import (
    Ad,
    Evidence,
    News,
    PortalUser,
    Reader,
    ReaderProfile,
    ReportedNews,
    Reporter,
    ReporterProfile,
    RewardGranted,
)

# Register your models here.
admin.site.register(
    [
        Ad,
        News,
        Reporter,
        ReporterProfile,
        PortalUser,
        Reader,
        ReaderProfile,
        RewardGranted,
    ]
)
