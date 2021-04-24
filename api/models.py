from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, \
    PageChooserPanel
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, StreamBlock, StructBlock, TextBlock, ListBlock, PageChooserBlock, IntegerBlock,
    RichTextBlock, )
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.documents.models import Document
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from accounts.models import PeopleCollection


class ClassBlock(StructBlock):
    outer = CharBlock(required=False)
    inner = CharBlock(required=False)


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
    classes = ClassBlock()
    text = CharBlock(required=True)
    page = PageChooserBlock(required=True)
    attrs = CharBlock(default='large rounded')

    class Meta:
        template = "blocks/button.html"


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)
    dimensions = CharBlock(required=False)

    class Meta:
        template = "blocks/image.html"


class ParagraphBlock(StructBlock):
    classes = ClassBlock()
    text = TextBlock(required=False)

    class Meta:
        template = "blocks/paragraph.html"


class CardBlock(StructBlock):
    classes = ClassBlock()
    image = ImageBlock()
    title = CharBlock(required=True)
    paragraph = ParagraphBlock()
    page = PageChooserBlock(required=False)
    buttons = ListBlock(ButtonBlock)
    attrs = CharBlock(default='tile flat')

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


class BlockQuote(StructBlock):
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


class HeroBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    title = CharBlock(required=True)
    subtitle = TextBlock(required=False)
    height = CharBlock(required=True, default='700px')
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
    classes = ClassBlock()
    cards = ListBlock(CardBlock)

    class Meta:
        template = "blocks/grid_of_cards.html"


class CarouselBlock(StructBlock):
    carousel_items = ListBlock(HeroBlock)

    class Meta:
        template = "blocks/carousel.html"


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
    groupings = models.CharField(max_length=50, blank=True)
    pre_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)
    classes_outer = models.CharField(max_length=200, blank=True)
    classes_inner = models.CharField(max_length=200, blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('pre_stream_body'),
            FieldPanel('groupings'),
            FieldPanel('classes_outer'),
            FieldPanel('classes_inner'),
        ], "Look and feel"),
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


class PeoplePage(Page):
    pre_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)
    people_collection = models.ForeignKey(PeopleCollection, null=True, blank=False, on_delete=models.SET_NULL)
    post_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)
    classes_outer = models.CharField(max_length=200, blank=True)
    classes_inner = models.CharField(max_length=200, blank=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('pre_stream_body'),
        MultiFieldPanel([
            FieldPanel('people_collection', classname="full"),
            FieldPanel('classes_outer'),
            FieldPanel('classes_inner'),
        ], 'People'),
        StreamFieldPanel('post_stream_body'),
    ]


class DocumentsPage(Page):
    pre_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)
    documents = ParentalManyToManyField(Document, blank=True)
    post_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)
    classes_outer = models.CharField(max_length=200, blank=True)
    classes_inner = models.CharField(max_length=200, blank=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('pre_stream_body'),
        MultiFieldPanel([
            FieldPanel('documents', widget=forms.CheckboxSelectMultiple),
            FieldPanel('classes_outer'),
            FieldPanel('classes_inner'),
        ], 'Documents'),
        StreamFieldPanel('post_stream_body'),
    ]


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

    social_heading = models.CharField(max_length=140, blank=True, default='We\'re social')
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    extra_head_content = models.TextField(blank=True)

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    favicons = models.ManyToManyField(Favicon, blank=True)
    primary_color_hex = models.CharField(max_length=15, blank=True)
    secondary_color_hex = models.CharField(max_length=15, blank=True)
    background_color_class = models.CharField(max_length=15, blank=True, default='w3-light-grey')
    font_size = models.CharField(max_length=15, blank=True, default=1, null=True)

    show_site_name = models.BooleanField(default=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('social_heading'),
            FieldPanel('linkedin', classname='col6'),
            FieldPanel('facebook', classname='col6'),
            FieldPanel('twitter', classname='col6'),
            FieldPanel('instagram', classname='col6'),
            FieldPanel('youtube', classname='col6'),
        ], 'Social Media'),
        MultiFieldPanel([
            FieldPanel('address_1'),
            FieldPanel('address_2'),
            FieldPanel('city', classname='col6'),
            FieldPanel('country', classname='col6'),
        ], 'Address'),
        MultiFieldPanel([
            FieldPanel('extra_head_content'),
        ], 'Setup'),
        MultiFieldPanel([
            ImageChooserPanel('logo', ),
            FieldPanel('font_size', classname='col6'),
            FieldPanel('background_color_class', classname='col6'),
            FieldPanel('primary_color_hex', classname='col6'),
            FieldPanel('show_site_name', classname='col6'),
            FieldPanel('secondary_color_hex', classname='col6'),
        ], 'Basic settings'),
    ]

    # api - standard
    # about us  - standard page - include team
    # books  - standard page
    # authors  - standard page
    # events/announcements  - standard page
    # blog  - listing page
    # contact us - form page


@register_snippet
class PostCollection(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class BlogStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")


class BlogPeopleRelationship(Orderable, models.Model):
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'accounts.People', related_name='person_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('people')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPage(Page):
    introduction = models.TextField(help_text='Text to describe the page', blank=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
                              help_text='Landscape mode only; horizontal width between 1000px and 3000px.')
    body = StreamField(
        BlogStreamBlock(), verbose_name="Page body", blank=True
    )
    subtitle = models.CharField(blank=True, max_length=255)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date_published = models.DateField("Date article published", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('introduction', classname="full"),
        FieldPanel('is_featured'),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
        InlinePanel('blog_person_relationship', label="Author(s)", panels=None, min_num=1),
        FieldPanel('tags'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    def authors(self):
        authors = [
            n.people for n in self.blog_person_relationship.all()
        ]

        return authors


class BlogIndexPage(Page):
    pre_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)
    post_stream_body = StreamField(StandardStreamBlock(), blank=True, null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('pre_stream_body'),
        StreamFieldPanel('post_stream_body'),
    ]

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        posts = BlogPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        context['featured_posts'] = posts.filter(is_featured=True)
        context['posts'] = posts
        return context

    def serve_preview(self, request, mode_name):
        return self.serve(request)


class SelassieMensahIndex(BlogIndexPage):
    about_me_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='+')
    about_me_text = models.TextField(blank=True)
    about_me_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    more_posts_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='+')

    content_panels = Page.content_panels + [
        StreamFieldPanel('pre_stream_body'),
        ImageChooserPanel('about_me_image'),
        FieldPanel('about_me_text'),
        PageChooserPanel('about_me_page'),
        StreamFieldPanel('post_stream_body'),
        PageChooserPanel('more_posts_page'),
    ]
