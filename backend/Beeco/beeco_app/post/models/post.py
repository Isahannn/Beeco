from .base_post import BasePost
from ...managers import PostManager
from django.utils.translation import gettext_lazy as _

class Post(BasePost):
    objects = PostManager()

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = BasePost.Type.POST
        super().save(*args, **kwargs)
