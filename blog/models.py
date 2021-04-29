from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel

from wagtail.core import fields

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndex(Page):
    template = 'blog/index.html'

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndex, self).get_context(request)
        context['posts'] = ArticlePage.objects.child_of(self).live()
        return context


class ArticlePage(Page):
    template = 'blog/article_page.html'

    body = fields.RichTextField()
    date = models.DateTimeField("Post date")
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname='full'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, 'Common page configuration'),
        ImageChooserPanel('thumbnail')
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = []



    class Meta:
        verbose_name = 'Article Page'
        verbose_name_plural = 'Article Pages'
