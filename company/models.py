from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Company(models.Model):
    director = models.OneToOneField(CustomUser, related_name='my_company', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    image = models.ImageField(upload_to='company/', blank=True, null=True)
    inn = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class CompanyAddress(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    email = models.EmailField(blank=True, null=True)
    tel1 = models.CharField(max_length=13)
    tel2 = models.CharField(max_length=13)
    map_url = models.URLField()
    main_add = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.company.title}"



