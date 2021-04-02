from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, \
    TabbedInterface, ObjectList
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

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


@register_snippet
class Favicon(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    panels = [
        ImageChooserPanel('image'),
    ]


@register_setting
class Configuration(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', blank=True)
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @', blank=True)
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL', blank=True)
    favicons = models.ManyToManyField(Favicon, blank=True)
    primary_color = models.CharField(max_length=15, blank=True)
    secondary_color = models.CharField(max_length=15, blank=True)

    social_media_panels = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('youtube'),
    ]

    site_setup = [
        FieldPanel('favicons'),
        FieldPanel('primary_color'),
        FieldPanel('secondary_color'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(site_setup, heading='Site configuration'),
        ObjectList(social_media_panels, heading='Social Media'),
    ])

# home - standard
# about us  - standard page - include team
# books  - standard page
# authors  - standard page
# events/announcements  - standard page
# blog  - listing page
# contact us - form page
