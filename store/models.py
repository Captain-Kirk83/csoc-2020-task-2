from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    description = models.TextField(null=True)
    mrp = models.PositiveIntegerField()
    rating = models.FloatField(default=0.0)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} by {self.author}'


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=True, blank=True)
    # True status means that the copy is available for issue, False means unavailable
    status = models.BooleanField(default=True)
    borrower = models.ForeignKey(User, related_name='borrower', null=True, blank=True, on_delete=models.SET_NULL)
    
    def saves(self,i,j,k):
        print(i,j,k)
        self.status=i
        self.borrow_date=k;
        self.borrower=j;
        models.Model.save(self)
    def __str__(self):
        if self.borrow_date:
            return f'{self.book.title}, {str(self.borrow_date)}'
        else:
            return f'{self.book.title} - Available'

class RateModel(models.Model):


    REVIEWS= (
        ('10', '10'),
        ('9', '9'),
        ('8', '8'),
        ('7', '7'),
        ('6', '6'),
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
        ('0', '0'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booktoRate = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookRate = models.PositiveIntegerField( choices=REVIEWS, default="10")

    class Meta:
        verbose_name_plural = 'rating'

    def __str__(self):
        return str(self.booktoRate)
