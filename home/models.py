from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from sedesel.blocks import StandardStreamBlock


class StandardPage(Page):
    introduction = models.TextField(blank=True)
    body = StreamField(StandardStreamBlock(), blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
    ]
