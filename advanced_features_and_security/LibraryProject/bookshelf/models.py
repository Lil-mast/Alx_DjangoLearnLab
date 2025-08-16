from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

def __str__(self):
        return self.title

class CustomUser:
    username = None  # Remove username field (use email instead)
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    USERNAME_FIELD = 'email'  # Use email as login identifier
    REQUIRED_FIELDS = []      # Remove email from REQUIRED_FIELDS

    objects = CustomUserManager()

    def __str__(self):
        return self.email