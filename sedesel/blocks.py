from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, StreamBlock, StructBlock, TextBlock, ListBlock, PageChooserBlock, RichTextBlock, )
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        template = "blocks/heading.html"


class ButtonBlock(StructBlock):
    text = CharBlock(required=True)
    page = PageChooserBlock(required=True)

    class Meta:
        template = "blocks/button.html"


class CardBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    title = CharBlock(required=True)
    text = TextBlock(required=False, max_length=450)
    page = PageChooserBlock(required=False)
    buttons = ListBlock(ButtonBlock)

    class Meta:
        template = "blocks/card.html"


class IntroducerBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    image_position = ChoiceBlock(default='left', choices=[
        ('left', 'Left'),
        ('right', 'Right'),
    ], blank=True, required=True)
    title = CharBlock(required=True)
    text = TextBlock(required=False, max_length=450)
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
    title = CharBlock(required=True)
    subtitle = TextBlock(required=False)
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
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    embed = EmbedBlock()
    half_title_text = HalfTitleTextBlock()
