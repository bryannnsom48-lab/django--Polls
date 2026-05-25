import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date Published")
    is_closed = models.BooleanField(default=False)
    
    @property
    def total_votes(self):
        return sum(choice.votes for choice in self.choice_set.all())
    
    class Meta:
        indexes = [
            models.Index(fields=["question_text", "pub_date"])
        ]
        permissions = [
            ("close_question", "Can close a Poll"),
        ]
    
    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean = True,# Tells django to look at method result and choose icon
        ordering = "pub_date",# Tells which database field to use in sorting 
        description = "Published Recently",# This sets the column header text in the admin pannel
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class meta:
        #Forcesthe combination of user and question to be unique
        unique_together = ("user", "question")
        
    def __str__(self):
        return f"{self.user.username} voted on {self.question.question_text}"