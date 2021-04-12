# Generated by Django 2.2.18 on 2021-04-10 20:16

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
from django.db import migrations

import api.models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_auto_20210410_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='pre_stream_body',
            field=wagtail.core.fields.StreamField([('carousel', wagtail.core.blocks.StructBlock(
                [('carousel_items', wagtail.core.blocks.ListBlock(api.models.HeroBlock))])), ('hero',
                                                                                              wagtail.core.blocks.StructBlock(
                                                                                                  [('image',
                                                                                                    wagtail.images.blocks.ImageChooserBlock(
                                                                                                        required=False)),
                                                                                                   ('title',
                                                                                                    wagtail.core.blocks.CharBlock(
                                                                                                        required=True)),
                                                                                                   ('subtitle',
                                                                                                    wagtail.core.blocks.TextBlock(
                                                                                                        required=False)),
                                                                                                   ('height',
                                                                                                    wagtail.core.blocks.CharBlock(
                                                                                                        default='700px',
                                                                                                        required=True)),
                                                                                                   (
                                                                                                   'container_alignment',
                                                                                                   wagtail.core.blocks.ChoiceBlock(
                                                                                                       blank=True,
                                                                                                       choices=[(
                                                                                                                'w3-display-middle',
                                                                                                                'Center'),
                                                                                                                (
                                                                                                                'w3-display-left container',
                                                                                                                'Left'),
                                                                                                                (
                                                                                                                'w3-display-right container',
                                                                                                                'Right')])),
                                                                                                   ('text_alignment',
                                                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                                                        blank=True,
                                                                                                        choices=[(
                                                                                                                 'w3-center',
                                                                                                                 'Center'),
                                                                                                                 (
                                                                                                                 'w3-left-align',
                                                                                                                 'Left'),
                                                                                                                 (
                                                                                                                 'w3-right-align',
                                                                                                                 'Right')],
                                                                                                        editable=False)),
                                                                                                   ('buttons',
                                                                                                    wagtail.core.blocks.ListBlock(
                                                                                                        api.models.ButtonBlock))])),
                                                   ('introducer', wagtail.core.blocks.StructBlock([('classes',
                                                                                                    wagtail.core.blocks.StructBlock(
                                                                                                        [('outer',
                                                                                                          wagtail.core.blocks.CharBlock(
                                                                                                              required=False)),
                                                                                                         ('inner',
                                                                                                          wagtail.core.blocks.CharBlock(
                                                                                                              required=False))])),
                                                                                                   ('image',
                                                                                                    wagtail.core.blocks.StructBlock(
                                                                                                        [('image',
                                                                                                          wagtail.images.blocks.ImageChooserBlock(
                                                                                                              required=False)),
                                                                                                         ('caption',
                                                                                                          wagtail.core.blocks.CharBlock(
                                                                                                              required=False)),
                                                                                                         ('attribution',
                                                                                                          wagtail.core.blocks.CharBlock(
                                                                                                              required=False)),
                                                                                                         ('dimensions',
                                                                                                          wagtail.core.blocks.CharBlock(
                                                                                                              required=False))])),
                                                                                                   ('image_position',
                                                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                                                        blank=True,
                                                                                                        choices=[(
                                                                                                                 'left',
                                                                                                                 'Left'),
                                                                                                                 (
                                                                                                                 'right',
                                                                                                                 'Right')])),
                                                                                                   ('text',
                                                                                                    wagtail.core.blocks.TextBlock(
                                                                                                        required=False)),
                                                                                                   ('buttons',
                                                                                                    wagtail.core.blocks.ListBlock(
                                                                                                        api.models.ButtonBlock))])),
                                                   ('grid_of_cards', wagtail.core.blocks.StructBlock([('classes',
                                                                                                       wagtail.core.blocks.StructBlock(
                                                                                                           [('outer',
                                                                                                             wagtail.core.blocks.CharBlock(
                                                                                                                 required=False)),
                                                                                                            ('inner',
                                                                                                             wagtail.core.blocks.CharBlock(
                                                                                                                 required=False))])),
                                                                                                      ('cards',
                                                                                                       wagtail.core.blocks.ListBlock(
                                                                                                           api.models.CardBlock))])),
                                                   ('padding', wagtail.core.blocks.StructBlock(
                                                       [('size', wagtail.core.blocks.IntegerBlock(required=True))])), (
                                                   'heading', wagtail.core.blocks.StructBlock([('classes',
                                                                                                wagtail.core.blocks.StructBlock(
                                                                                                    [('outer',
                                                                                                      wagtail.core.blocks.CharBlock(
                                                                                                          required=False)),
                                                                                                     ('inner',
                                                                                                      wagtail.core.blocks.CharBlock(
                                                                                                          required=False))])),
                                                                                               ('title',
                                                                                                wagtail.core.blocks.CharBlock(
                                                                                                    required=True)), (
                                                                                               'size',
                                                                                               wagtail.core.blocks.ChoiceBlock(
                                                                                                   blank=True, choices=[
                                                                                                       ('',
                                                                                                        'Select a header size'),
                                                                                                       ('h2', 'H2'),
                                                                                                       ('h3', 'H3'),
                                                                                                       ('h4', 'H4')],
                                                                                                   required=False)), (
                                                                                               'subtitle',
                                                                                               wagtail.core.blocks.CharBlock(
                                                                                                   required=False))])),
                                                   ('paragraph', wagtail.core.blocks.StructBlock([('classes',
                                                                                                   wagtail.core.blocks.StructBlock(
                                                                                                       [('outer',
                                                                                                         wagtail.core.blocks.CharBlock(
                                                                                                             required=False)),
                                                                                                        ('inner',
                                                                                                         wagtail.core.blocks.CharBlock(
                                                                                                             required=False))])),
                                                                                                  ('text',
                                                                                                   wagtail.core.blocks.TextBlock(
                                                                                                       required=False))])),
                                                   ('embed', wagtail.embeds.blocks.EmbedBlock()), ('half_title_text',
                                                                                                   wagtail.core.blocks.StructBlock(
                                                                                                       [('heading',
                                                                                                         wagtail.core.blocks.StructBlock(
                                                                                                             [(
                                                                                                              'classes',
                                                                                                              wagtail.core.blocks.StructBlock(
                                                                                                                  [(
                                                                                                                   'outer',
                                                                                                                   wagtail.core.blocks.CharBlock(
                                                                                                                       required=False)),
                                                                                                                   (
                                                                                                                   'inner',
                                                                                                                   wagtail.core.blocks.CharBlock(
                                                                                                                       required=False))])),
                                                                                                              ('title',
                                                                                                               wagtail.core.blocks.CharBlock(
                                                                                                                   required=True)),
                                                                                                              ('size',
                                                                                                               wagtail.core.blocks.ChoiceBlock(
                                                                                                                   blank=True,
                                                                                                                   choices=[
                                                                                                                       (
                                                                                                                       '',
                                                                                                                       'Select a header size'),
                                                                                                                       (
                                                                                                                       'h2',
                                                                                                                       'H2'),
                                                                                                                       (
                                                                                                                       'h3',
                                                                                                                       'H3'),
                                                                                                                       (
                                                                                                                       'h4',
                                                                                                                       'H4')],
                                                                                                                   required=False)),
                                                                                                              (
                                                                                                              'subtitle',
                                                                                                              wagtail.core.blocks.CharBlock(
                                                                                                                  required=False))])),
                                                                                                        ('paragraph',
                                                                                                         wagtail.core.blocks.StructBlock(
                                                                                                             [(
                                                                                                              'classes',
                                                                                                              wagtail.core.blocks.StructBlock(
                                                                                                                  [(
                                                                                                                      'outer',
                                                                                                                      wagtail.core.blocks.CharBlock(
                                                                                                                          required=False)),
                                                                                                                      (
                                                                                                                          'inner',
                                                                                                                          wagtail.core.blocks.CharBlock(
                                                                                                                              required=False))])),
                                                                                                                 (
                                                                                                                 'text',
                                                                                                                 wagtail.core.blocks.TextBlock(
                                                                                                                     required=False))]))]))],
                                                  blank=True,
                                                  null=True),
        ),
    ]