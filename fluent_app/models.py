from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class ConversationTemplate(models.Model):
    class Language(models.TextChoices):
        ENGLISH = 'en', 'English'

    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.ENGLISH,
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    context = models.JSONField(default=list)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    template = models.ForeignKey(
        ConversationTemplate,
        null=True,
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    log = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'{self.template.name} by {self.user.username}'

    def save(self, *args, **kwargs):
        if len(self.log) == 0:
            self.log = self.template.context
        super(Conversation, self).save(*args, **kwargs)
