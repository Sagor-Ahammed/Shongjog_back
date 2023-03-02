from django.db import models
from django.db import models
from django.contrib.auth.models import User 
import PIL
from PIL import Image

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #image compresser
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.image.path)
        
        myHeight, myWidth = img.size 
        img = img.resize((myHeight,myWidth) , PIL.Image.LANCZOS)
        img.save(self.image.path)
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
