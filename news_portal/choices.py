from django.db.models import TextChoices


class UserTypes(TextChoices):
    ADMIN = "Admin", "ADMIN"
    READER = "Reader", "READER"
    REPORTER = "Reporter", "REPORTER"


GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("non-binary", "Non-binary"),
)

SOURCE_CHOICES = (
    ("personal", "Personal Reporting"),
    ("agency", "News Agency"),
)


class NewsCategory(TextChoices):
    SPORTS = "sports", "Sports"
    POLITICS = "politics", "Politics"
    FINANACE = "finance", "Finance"
    INTERNATIONAL = "international", "International"


PACKAGE_CHOICES = (
    ("bronz", "Bronz"),
    ("silver", "Silver"),
    ("gold", "Gold"),
)

REPORTED_STATUS = (
    ("pending", "Pending"),
    ("denied", "Denied"),
    ("accepted", "Accepted"),
)
