from django.db import models
from django.utils.translation import gettext_lazy as _
from Beeco.beeco_app.posts import BasePost
from django.core.validators import MinValueValidator


class Group(BasePost):
    max_members = models.PositiveIntegerField(
        _('Максимальное количество участников'),
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text=_("Минимальное значение: 1")
    )
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=BasePost.Status.choices,
        default=BasePost.Status.OPEN
    )

    group_members = models.ManyToManyField(
        'User',
        related_name='groups',
        blank=True,
        verbose_name=_('Участники группы')
    )

    objects = GroupMemberManager()

    class Meta:
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')

    def save(self, *args, **kwargs):
        self.type = BasePost.Type.GROUP
        super().save(*args, **kwargs)

    def can_user_join(self, user):
        if self.status != self.Status.OPEN:
            return False
        if self.max_members and self.group_members.count() >= self.max_members:
            return False
        return not self.group_members.filter(id=user.id).exists()
