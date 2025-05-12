# #* import uuid
# from polymorphic.models import PolymorphicModel
# from django.db import models
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from .managers import CustomUserManager, PostManager, GroupMemberManager
# from django.core.validators import MinValueValidator
#
#
# class User(AbstractUser):
#         username = None
#
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         email = models.EmailField(_('email address'), unique=True, db_index=True)
#         first_name = models.CharField(_('first name'), max_length=100)
#         last_name = models.CharField(_('last name'), max_length=100)
#         nickname = models.CharField(_('nickname'), max_length=100, unique=True, db_index=True)
#         location = models.CharField(_('location'), max_length=30, blank=True)
#         date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
#         avatar = models.ImageField(
#             _('avatar'),
#             upload_to='avatars/',
#             null=True,
#             blank=True,
#             help_text=_('Profile picture')
#         )
#
#         date_joined = models.DateTimeField(_('date joined'), default=timezone.now, db_index=True)
#         is_staff = models.BooleanField(
#             _('staff status'),
#             default=False,
#             help_text=_('Designates whether the user can log into this admin site.'),
#             db_index=True
#         )
#         is_active = models.BooleanField(
#             _('active'),
#             default=True,
#             help_text=_(
#                 'Designates whether this user should be treated as active. '
#                 'Unselect this instead of deleting accounts.'
#             ),
#             db_index=True
#         )
#
#         USERNAME_FIELD = 'email'
#         REQUIRED_FIELDS = ['first_name', 'last_name', 'nickname']
#
#         objects = CustomUserManager()
#
#         def __str__(self):
#             return self.email
#
#         @property
#         def full_name(self):
#             return f"{self.first_name} {self.last_name}"
#
#         class Meta:
#             verbose_name = _('user')
#             verbose_name_plural = _('users')
#             ordering = ['-date_joined']
#
#
# class Tag(models.Model):
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         name = models.CharField(_('name'), max_length=50, unique=True)
#         created_at = models.DateTimeField(_('created at'), default=timezone.now, db_index=True)
#
#         def __str__(self):
#             return self.name
#
#         class Meta:
#             verbose_name = _('tag')
#             verbose_name_plural = _('tags')
#             ordering = ['name']
#
#
# class BasePost(PolymorphicModel):
#         class Status(models.TextChoices):
#             OPEN = 'open', _('Открытая')
#             CLOSED = 'closed', _('Закрытая')
#             DRAFT = 'draft', _('Черновик')
#
#         class Type(models.TextChoices):
#             POST = 'post', _('Пост')
#             GROUP = 'group', _('Группа')
#
#         id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#         title = models.CharField(_('Заголовок'), max_length=100, blank=True)
#         user = models.ForeignKey(
#             'User',
#             on_delete=models.CASCADE,
#             null=True,
#             blank=True,
#             related_name='%(class)s'
#         )
#         description = models.TextField(_('Описание'), blank=True)
#         created_at = models.DateTimeField(_('Дата создания'), default=timezone.now, db_index=True)
#         updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
#         tags = models.ManyToManyField(
#             'Tag',
#             related_name='%(class)s',
#             blank=True,
#             verbose_name=_('Теги')
#         )
#         type = models.CharField(max_length=10, choices=Type.choices, default=Type.POST, null=False, editable=False)
#
#         objects = models.Manager()
#
#         class Meta:
#             abstract = True
#             ordering = ['-created_at']
#             verbose_name = _('базовый пост')
#             verbose_name_plural = _('базовые посты')
#
#         def __str__(self):
#             return self.title
#
#
# class Post(BasePost):
#         objects = PostManager()
#
#         class Meta:
#             verbose_name = _('пост')
#             verbose_name_plural = _('посты')
#
#         def save(self, *args, **kwargs):
#             if not self.type:
#                 self.type = BasePost.Type.POST
#             super().save(*args, **kwargs)
#
# class Comment(models.Model):
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#         post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='comments')
#         parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
#         text = models.TextField(_('text'))
#         created_at = models.DateTimeField(_('created at'), default=timezone.now, db_index=True)
#         updated_at = models.DateTimeField(_('updated at'), auto_now=True)
#
#         class Meta:
#             ordering = ['-created_at']
#             verbose_name = _('comment')
#             verbose_name_plural = _('comments')
#
#         def __str__(self):
#             return f"Comment by {self.user} on {self.post}"
#
#
# class Group(BasePost):
#         max_members = models.PositiveIntegerField(
#             _('max members'),
#             null=True,
#             blank=True,
#             validators=[MinValueValidator(1)],
#             help_text=_("Минимальное значение: 1")
#         )
#         status = models.CharField(
#             _('status'),
#             max_length=20,
#             choices=BasePost.Status.choices,
#             default=BasePost.Status.OPEN
#         )
#
#         objects = GroupMemberManager()
#
#         class Meta:
#             verbose_name = _('group')
#             verbose_name_plural = _('groups')
#
#         def save(self, *args, **kwargs):
#             self.type = BasePost.Type.GROUP
#             super().save(*args, **kwargs)
#
#         def can_user_join(self, user):
#             if self.status != self.Status.OPEN:
#                 return False
#             if self.max_members and self.group_members.count() >= self.max_members:
#                 return False
#             return not self.group_members.filter(user=user).exists()
#
# class GroupMember(models.Model):
#         class Role(models.TextChoices):
#             MEMBER = 'member', _('Участник')
#             ADMIN = 'admin', _('Администратор')
#
#         id = models.UUIDField(
#             primary_key=True,
#             default=uuid.uuid4,
#             editable=False,
#             verbose_name='ID'
#         )
#         group = models.ForeignKey(
#             'Group',
#             on_delete=models.CASCADE,
#             related_name='group_members',
#             verbose_name=_('группа')
#         )
#         user = models.ForeignKey(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.CASCADE,
#             related_name='group_memberships',
#             verbose_name=_('пользователь')
#         )
#         role = models.CharField(
#             max_length=10,
#             choices=Role.choices,
#             default=Role.MEMBER,
#             verbose_name=_('роль')
#         )
#         joined_at = models.DateTimeField(
#             auto_now_add=True,
#             verbose_name=_('дата присоединения'),
#             db_index=True
#         )
#
#         class Meta:
#             verbose_name = _('участник группы')
#             verbose_name_plural = _('участники групп')
#
#             ordering = ['-joined_at']
#
#         def __str__(self):
#             return f"{self.user} в {self.group} (роль: {self.role})"
#
# class Like(models.Model):
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#         post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='likes')
#         created_at = models.DateTimeField(_('created at'), default=timezone.now, db_index=True)
#
#         class Meta:
#             constraints = [
#                 models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
#             ]
#             verbose_name = _('like')
#             verbose_name_plural = _('likes')
#
#         def __str__(self):
#             return f"Like by {self.user} on {self.post}"
#
# class Notification(models.Model):
#         class NotificationType(models.TextChoices):
#             LIKE = 'like', _('Like')
#             COMMENT = 'comment', _('Comment')
#             GROUP_INVITE = 'group_invite', _('Group Invite')
#
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#         sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
#         notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
#         content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#         object_id = models.UUIDField()
#         content_object = GenericForeignKey('content_type', 'object_id')
#         is_read = models.BooleanField(default=False)
#         created_at = models.DateTimeField(_('created at'), default=timezone.now, db_index=True)
#
#         class Meta:
#             ordering = ['-created_at']
#             verbose_name = _('notification')
#             verbose_name_plural = _('notifications')
#
#         def __str__(self):
#             return f"{self.notification_type} notification for {self.recipient}"
#
#
# class Chat(models.Model):
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         participants = models.ManyToManyField(User, related_name='chats')
#         created_at = models.DateTimeField(default=timezone.now, db_index=True)
#         updated_at = models.DateTimeField(auto_now=True)
#
#         class Meta:
#             ordering = ['-updated_at']
#
# class ChatMessage(models.Model):
#         id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
#         sender = models.ForeignKey(User, on_delete=models.CASCADE)
#         text = models.TextField()
#         created_at = models.DateTimeField(default=timezone.now, db_index=True)
#         is_read = models.BooleanField(default=False)
#
#         class Meta:
#             ordering = ['created_at']
#
#         def __str__(self):
#             return f"Message by {self.sender} in chat {self.chat.id}"
#