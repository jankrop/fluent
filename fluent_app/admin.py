from django.contrib import admin

from fluent_app.models import Conversation, ConversationTemplate

admin.site.register(Conversation)
admin.site.register(ConversationTemplate)
