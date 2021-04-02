from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page

from sedesel.blocks import StandardStreamBlock


class StandardPage(Page):
    introduction = models.TextField(blank=True)
    body = StreamField(StandardStreamBlock(), blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
    ]


class FormPage(AbstractEmailForm):
    submit_cta = models.CharField(max_length=140, help_text='Example: Submit, Save, Go!')
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('submit_cta'),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)

# home - standard
# about us  - standard page - include team
# books  - standard page
# authors  - standard page
# events/announcements  - standard page
# blog  - listing page
# contact us - form page
