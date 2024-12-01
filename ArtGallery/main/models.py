from django.db import models

class Contact(models.Model):

    fname = models.CharField(max_length=128)
    lname = models.CharField(max_length=128)
    email = models.EmailField()
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"From: {self.fname} {self.lname}"