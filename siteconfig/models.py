from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User=get_user_model()

class Customblogname(models.Model):
    blogname=models.CharField(max_length=100)

    def __str__(self):
        return self.blogname

    class Meta:
        verbose_name_plural='Blog name'


class Ranks(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Stuff & Contacts Ranks'

class Contacts(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     rank=models.ForeignKey(Ranks,on_delete=models.CASCADE)
     phone=models.CharField(max_length=15)
     dateadded=models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f'{self.user.username},\n {self.rank.title} \n TEL:({self.phone})'

     class Meta:
        verbose_name_plural='Add Contacts'

class About(models.Model):
    street_address=models.TextField(max_length=255,default="Siriba campus - Nyawita")
    physical_location=models.CharField(max_length=255,default="Maseno Student Center - Left Side Pocket")
    email=models.EmailField(max_length=100,default="asiafric@gmail.com")
    tel=models.CharField(max_length=12,default="254711349412")
    facebook=models.URLField(default='facebook.com')
    twitter=models.URLField(default='twitter.com')
    youtube=models.URLField(default='youtube.com')
    instagram=models.URLField(default='instagram.com')
    tiktok = models.URLField(default='tiktok.com')
    linkedin = models.URLField(default='linkedin.com')
    other=models.URLField(default="enter any aditional social media url",blank=True,null=True)
    rights_year=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Organisation contacts and location"

    def __str__(self):
        return self.email

class Gallery(models.Model):
    image=models.ImageField(upload_to="gallery/images/%d/")
    timestamp=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.image.url

    class Meta:
        ordering=['-timestamp']
        verbose_name_plural="Gallery"


class Site_Policies(models.Model):
    terms=models.TextField(max_length=255,default='Add site terms and conditions here')
    privacy_policy=models.TextField(max_length=255,default='Add your privacy policy here')
    cookies_policy = models.TextField(max_length=255, default='Add your coockies policy here')
    adds_info = models.TextField(max_length=255, default='Add info')

    def __str__(self):
        return "Site Policies"
    class Meta:
        verbose_name_plural='Site Policies'


class ThirdParty(models.Model):
    third_party_name=models.CharField(max_length=100,default='TDBSoft')
    third_party_site=models.URLField(max_length=255,default='tdbsoft.pythonanywhere.com')
    third_party_phone = models.TextField(max_length=15, default='+254743793901')
    third_party_email = models.EmailField(max_length=255, default='infotdbsoft@gmail.com')

    def __str__(self):
        return self.third_party_name

    class Meta:
        verbose_name_plural='Third Party'

class FQA(models.Model):
    question=models.TextField(max_length=255,default='Question 1')
    answer=models.TextField(max_length=255,default='Answer for question 1')

    def __str__(self):
        return f'Question:{self.question}? \n - Answer:{self.answer}'

class Howitworks(models.Model):
    title=models.CharField(max_length=100,default='Title')
    content=models.TextField(max_length=255,default='Content')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'How it works'



