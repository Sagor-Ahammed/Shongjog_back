from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userfriend')
    friends = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')

    def __str__(self):
        return self.user.username + ' is friends with ' + self.friends.username

class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userfriendrequest')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_to', null=True, blank=True)
    received_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_from', null=True, blank=True)

    def __str__(self):
        return self.user.username

