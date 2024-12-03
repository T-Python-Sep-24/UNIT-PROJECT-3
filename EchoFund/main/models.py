from django.db import models

# Create your models here.


class Contact(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()


class Testimonial(models.Model):

    class Rates(models.IntegerChoices):

        STAR1 = 1, 'One Star'
        STAR2 = 2, 'Two Stars'
        STAR3 = 3, 'Three Stars'
        STAR4 = 4, 'Four Stars'
        STAR5 = 5, 'Five Stars'

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/avatars', default='images/avatars/profileAvatar.jpg', blank=True)
    subject = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.SmallIntegerField(choices=Rates.choices)
    rated_at = models.DateTimeField(auto_now_add=True)
