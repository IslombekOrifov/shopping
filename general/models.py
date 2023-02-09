from django.db import models
from ckeditor.fields import RichTextField


class Currency(models.Model):
    author = models.ForeignKey('accounts.CustomUser', related_name='currencies', on_delete=models.PROTECT)
    who_updated = models.ForeignKey('accounts.CustomUser', related_name='updated_currencies', on_delete=models.PROTECT)
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=20) # blankni o'chir
    symbol = models.CharField(max_length=2, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubscribeUs(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False)


class Faqs(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey('accounts.UserDataOnDelete', on_delete=models.CASCADE, blank=True, null=True)
    who_updated = models.ForeignKey('accounts.CustomUser', related_name='faqs_updated', on_delete=models.PROTECT)
    question = models.CharField(max_length=300)
    answer = RichTextField()
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class Contact(models.Model):
    url = models.URLField(blank=True)
    address = models.CharField(max_length=150)
    info_email = models.EmailField()
    career_email = models.EmailField(blank=True)
    working_time_start = models.CharField(max_length=50)
    working_time_end = models.CharField(max_length=50)
    phone = models.CharField(max_length=18)
    phone2 = models.CharField(max_length=18)
    summary_for_message = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)


class AboutUs(models.Model):
    quoute = models.CharField(max_length=300)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey('accounts.UserDataOnDelete', on_delete=models.CASCADE, blank=True, null=True)
    who_updated = models.ForeignKey('accounts.CustomUser', related_name='aboutus_updated', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)


class AboutUsThing(models.Model):
    about = models.ForeignKey(AboutUs, related_name='things', on_delete=models.PROTECT)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey('accounts.UserDataOnDelete', on_delete=models.CASCADE, blank=True, null=True)
    who_updated = models.ForeignKey('accounts.CustomUser', related_name='aboutus_thing_updated', on_delete=models.PROTECT)

    title = models.CharField(max_length=50)
    body = models.CharField(max_length=150)
    image = models.ImageField(upload_to='aboutus')
    is_active = models.BooleanField(default=True)


class AboutUsPlus(models.Model):
    about = models.ForeignKey(AboutUs, related_name='pluss', on_delete=models.PROTECT)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey('accounts.UserDataOnDelete', on_delete=models.CASCADE, blank=True, null=True)
    who_updated = models.ForeignKey('accounts.CustomUser', related_name='aboutus_plus_updated', on_delete=models.PROTECT)

    title = models.CharField(max_length=50)
    body = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)


class AboutUsGroup(models.Model):
    about = models.ForeignKey(AboutUs, related_name='groups', on_delete=models.PROTECT)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    author_data = models.ForeignKey('accounts.UserDataOnDelete', on_delete=models.CASCADE, blank=True, null=True)
    who_updated = models.ForeignKey('accounts.CustomUser', related_name='aboutus_group_updated', on_delete=models.PROTECT)

    person = models.ForeignKey('accounts.CustomUser', related_name='about_group', on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)