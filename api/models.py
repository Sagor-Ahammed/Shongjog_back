import os

from django.db import models
from django.db import models
from django.contrib.auth.models import User 
import PIL
from PIL import Image
from rest_framework.exceptions import ValidationError


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = PIL.Image.open(self.image.path)
            myHeight, myWidth = img.size
            img = img.resize((myHeight, myWidth), PIL.Image.LANCZOS)
            img.save(self.image.path)

    def clean(self):
        super().clean()
        if self.video:
            # check the video file size
            max_video_size = 10 * 1024 * 1024  #10mb
            if self.video.size > max_video_size:
                raise ValidationError(f"Video file size exceeds the limit of {max_video_size} bytes.")
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class profile_picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = PIL.Image.open(self.image.path)
            myHeight, myWidth = img.size
            img = img.resize((myHeight, myWidth), PIL.Image.LANCZOS)
            img.save(self.image.path)