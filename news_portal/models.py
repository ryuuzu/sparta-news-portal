from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Signal Imports
from django.dispatch import receiver
from django.db.models.signals import post_save
# Local Imports
from .choices import Types, GENDER_CHOICES, SOURCE_CHOICES, NEWS_CATEGORY, PACKAGE_CHOICES, REPORTED_STATUS
from .user_managers import ReaderManager, ReporterManager, PortalUserManager


# Create your models here.
class PortalUser(AbstractBaseUser):
    type = models.CharField(max_length=25, choices=Types.choices, default=Types.READER)

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    # mandatory fields if inherited from AbstractUser
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # additional common users fields
    first_name = models.CharField(max_length=100, verbose_name="First Name", null=True, blank=True)
    middle_name = models.CharField(
        max_length=100, verbose_name="Middle Name", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", null=True, blank=True)
    gender = models.CharField(max_length=20,
                              verbose_name="Gender", choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    contact_number = models.CharField(
        max_length=10, verbose_name="Contact Number", null=True, blank=True)
    photo = models.ImageField(
        verbose_name="User Photo", null=True, blank=True, upload_to="photos")
    
    city = models.CharField(
        max_length=50, verbose_name="Permanent Address", null=True, blank=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['']

    objects = PortalUserManager()

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.type or self.type == None:
            self.type = Types.ADMIN
        return super().save(*args, **kwargs)

class Reporter(PortalUser):
    class Meta:
        proxy = True
    objects=ReporterManager()
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Types.REPORTER
        return super().save(*args, **kwargs)

class Reader(PortalUser):
    class Meta:
        proxy = True
    objects=ReaderManager()
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Types.READER
        return super().save(*args, **kwargs)

class ReaderProfile(models.Model):
    # user = models.OneToOneField(PortalUser, on_delete=models.CASCADE)
    pass    

class ReporterProfile(models.Model):
    user = models.OneToOneField(PortalUser, on_delete=models.CASCADE)
    press_id = models.ImageField(
        verbose_name="Press ID", null=True, blank=True, upload_to="photos")
    identity_document = models.ImageField(
        verbose_name="Identity Document", null=True, blank=True, upload_to="photos")


@receiver(post_save, sender=Reporter)
@receiver(post_save, sender=Reader)
def create_all_profiles(sender, instance, **kwargs):
    if sender == Reporter:
        ReporterProfile.objects.create(user=instance)
    elif sender == Reader:
        ReaderProfile.objects.create(user=instance)
    else:
        pass

class News(models.Model):
    created_by = models.OneToOneField(Reporter, on_delete=models.PROTECT)
    title = models.CharField(max_length=1000)
    sub_title = models.CharField(max_length=1000)
    body = models.TextField()
    image1 = models.ImageField(blank=True, null=True, upload_to="photos")
    image2 = models.ImageField(blank=True, null=True, upload_to="photos")
    image3 = models.ImageField(blank=True, null=True, upload_to="photos")
    source = models.CharField(max_length=100,choices=SOURCE_CHOICES)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=NEWS_CATEGORY)
    upload_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    view_count = models.BigIntegerField(default=0)
    coin_generated = models.BigIntegerField(default=0)


class Evidence(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="photos")
    file1 = models.FileField(upload_to="documents")
    file2 = models.FileField(blank=True, null=True, upload_to="documents")


class Comment(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Reader, on_delete=models.CASCADE)
    comment = models.TextField()


class Ad(models.Model):
    company = models.CharField(max_length=250)
    contact = models.CharField(max_length=25)
    image = models.ImageField(upload_to="photos")
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()


class ReportedNews(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Reader, on_delete=models.CASCADE)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=REPORTED_STATUS)


class RewardGranted(models.Model):
    user_id = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    coins_redeemed = models.CharField(max_length=25)
    monetary_value = models.CharField(max_length=25)