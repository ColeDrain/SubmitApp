from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown
from datetime import datetime
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=150)
    upload_date = models.DateField(auto_now_add=True)

    question_type_choices =(
        ('M', 'Maths'),
        ('E', 'English'),
    )
    question_type = models.CharField(max_length=1, choices=question_type_choices)

    def is_deadline(self):
        return datetime.now().hour >= 18

    def __str__(self):
        return self.question_text

class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solution_text = models.TextField()
    image = models.ImageField(upload_to='images/')
    upload_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Submission by {self.author}'

    def get_text_as_markdown(self):
        return mark_safe(markdown(self.solution_text, safe_mode='escape'))
