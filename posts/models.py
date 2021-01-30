from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=350)
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField(max_length=350)
    author = models.CharField(max_length=50)

    def __str__(self):
        return f'post:{self.post.title},comment:{self.text},author:{self.author}'
