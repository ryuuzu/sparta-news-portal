from django.db.models import TextChoices

class Types(TextChoices):
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

NEWS_CATEGORY = (
    ("sports", "Sports"),
    ("politics", "Politics"),
    ("finance", "Finance"),
    ("international", "International"),
)

PACKAGE_CHOICES = (
    ('bronz', 'Bronz'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
)

REPORTED_STATUS = (
    ('pending', 'Pending'),
    ('denied', 'Denied'),
    ('accepted', 'Accepted'),
)