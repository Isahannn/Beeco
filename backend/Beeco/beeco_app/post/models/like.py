from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('beeco_app.Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']
        verbose_name = _('like')
        verbose_name_plural = _('likes')

    def __str__(self):
        return f"{self.user} liked {self.post}"