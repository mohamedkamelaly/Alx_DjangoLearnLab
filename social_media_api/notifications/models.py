from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Notificiations(models.Model):
    receipt = models.ForeignKey(CustomUser, on_delete=models.PROTECT,related_name='notifications')
    actor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='actions')
    verb = models.TextField()
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.actor} {self.verb} {self.target} to {self.recipient}'
