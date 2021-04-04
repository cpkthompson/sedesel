from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, StreamBlock, StructBlock, TextBlock, ListBlock, PageChooserBlock, RichTextBlock,
    BooleanBlock, IntegerBlock, )
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailstreamforms.blocks import WagtailFormBlock


class ClassBlock(StructBlock):
    inner = CharBlock(required=False)
    outer = CharBlock(required=False)


class HeadingBlock(StructBlock):
    classes = ClassBlock()
    title = CharBlock(required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)
    subtitle = CharBlock(required=False)

    class Meta:
        template = "blocks/heading.html"


class PaddingBlock(StructBlock):
    size = IntegerBlock(required=True)

    class Meta:
        template = "blocks/padding.html"


class ButtonBlock(StructBlock):
    text = CharBlock(required=True)
    page = PageChooserBlock(required=True)

    class Meta:
        template = "blocks/button.html"


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)
    dimensions = CharBlock(required=False)

    class Meta:
        template = "blocks/image.html"


class CardBlock(StructBlock):
    image = ImageBlock()
    title = CharBlock(required=True)
    text = TextBlock(required=False, max_length=450)
    page = PageChooserBlock(required=False)
    buttons = ListBlock(ButtonBlock)
    is_flat = BooleanBlock(required=False)

    class Meta:
        template = "blocks/card.html"


class IntroducerBlock(StructBlock):
    classes = ClassBlock()
    image = ImageBlock()
    image_position = ChoiceBlock(default='left', choices=[
        ('left', 'Left'),
        ('right', 'Right'),
    ], blank=True, required=True)
    text = TextBlock(required=False)
    buttons = ListBlock(ButtonBlock)

    class Meta:
        template = "blocks/introducer.html"


class HeroBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    title = CharBlock(required=True)
    subtitle = TextBlock(required=False)
    container_alignment = ChoiceBlock(default='w3-display-middle', choices=[
        ('w3-display-middle', 'Center'),
        ('w3-display-left container', 'Left'),
        ('w3-display-right container', 'Right'),
    ], blank=True, required=True)
    text_alignment = ChoiceBlock(default='w3-center', choices=[
        ('w3-center', 'Center'),
        ('w3-left-align', 'Left'),
        ('w3-right-align', 'Right'),
    ], blank=True, required=True, editable=False)
    buttons = ListBlock(ButtonBlock)

    class Meta:
        template = "blocks/hero.html"


class GridOfCardsBlock(StructBlock):
    container_class = CharBlock()
    cards = ListBlock(CardBlock)

    class Meta:
        template = "blocks/grid_of_cards.html"


class CarouselBlock(StructBlock):
    carousel_items = ListBlock(HeroBlock)

    class Meta:
        template = "blocks/carousel.html"


class ParagraphBlock(StructBlock):
    text = RichTextBlock()

    class Meta:
        template = "blocks/paragraph.html"


class HalfTitleTextBlock(StructBlock):
    heading = HeadingBlock()
    paragraph = ParagraphBlock()

    class Meta:
        template = "blocks/half_title_text.html"


class StandardStreamBlock(StreamBlock):
    carousel = CarouselBlock()
    hero = HeroBlock()
    introducer = IntroducerBlock()
    grid_of_cards = GridOfCardsBlock()
    padding = PaddingBlock()
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    embed = EmbedBlock()
    half_title_text = HalfTitleTextBlock()
    form = WagtailFormBlock()


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


class MyFormField(AbstractFormField):
    grouping = models.CharField(max_length=140, blank=True)
    panels = AbstractFormField.panels + [
        FieldPanel('grouping'),
    ]


class FormField(MyFormField):
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
    address_1 = models.CharField(max_length=140, blank=True)
    address_2 = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=140, blank=True)
    country = models.CharField(max_length=140, blank=True)

    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    favicons = models.ManyToManyField(Favicon, blank=True)
    primary_color = models.CharField(max_length=15, blank=True)
    secondary_color = models.CharField(max_length=15, blank=True)
    font_size = models.CharField(max_length=15, blank=True, default=1, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('linkedin'),
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('instagram'),
        ], 'Social Media'),
        MultiFieldPanel([
            FieldPanel('address_1'),
            FieldPanel('address_2'),
            FieldPanel('city'),
            FieldPanel('country'),
        ], 'Address'),
        MultiFieldPanel([
            ImageChooserPanel('logo'),
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
            FieldPanel('font_size'),
        ], 'Basic settings'),
    ]

    # home - standard
    # about us  - standard page - include team
    # books  - standard page
    # authors  - standard page
    # events/announcements  - standard page
    # blog  - listing page
    # contact us - form page
