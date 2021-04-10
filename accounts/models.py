from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
# Create your models here.
from wagtail.snippets.models import register_snippet


@register_snippet
class PeopleCollection(index.Indexed, ClusterableModel):
    title = models.CharField("Title", max_length=254, null=True, blank=True)
    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title


@register_snippet
class People(index.Indexed, ClusterableModel):
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    headline = models.CharField("Headline", max_length=254, null=True, blank=True)
    collection = models.ManyToManyField(PeopleCollection, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    bio = models.TextField(blank=True)

    panels = [
        FieldPanel('user'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name"),
        FieldPanel('headline'),
        FieldPanel('collection'),
        ImageChooserPanel('photo'),
        FieldPanel('bio'),

    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_photo(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.photo.get_rendition('fill-50x50').img_tag()
        except:
            return ''

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['id']
