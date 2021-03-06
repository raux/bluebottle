from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.functional import lazy
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem
from fluent_contents.extensions.model_fields import PluginHtmlField, PluginImageField
from fluent_contents.models import PlaceholderField
from fluent_contents.models.db import ContentItem
from fluent_contents.models.fields import ContentItemRelation
from fluent_contents.models.managers import ContentItemManager
from fluent_contents.rendering import render_placeholder
from fluent_contents.utils.filters import apply_filters

from bluebottle.clients import properties
from bluebottle.utils.models import PublishableModel
from bluebottle.utils.serializers import MLStripper


def get_languages():
    return properties.LANGUAGES


class DocumentItem(ContentItem):

    text = models.CharField(_('Link title'), max_length=100)
    document = models.FileField(_("Document"), upload_to='pages')

    def __str__(self):
        return Truncator(strip_tags(self.text)).words(20)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Document')


class ImageTextItem(ContentItem):
    """
    A snippet of HTML text to display on a page.
    """
    text = PluginHtmlField(_('text'), blank=True)
    text_final = models.TextField(editable=False, blank=True, null=True)
    image = PluginImageField(_("Image"), upload_to='pages')

    ALIGN_CHOICES = (
        ('left', _("Left")),
        ('right', _("Right")),
    )

    RATIO_CHOICES = (
        (8, _("2:1 (Text twice as wide)")),
        (6, _("1:1 (Equal width)")),
        (4, _("1:2 (Image twice as wide)")),
    )

    align = models.CharField(_("Picture placement"), max_length=10, choices=ALIGN_CHOICES, blank=True)
    ratio = models.IntegerField(_("Picture / Text ratio"), choices=RATIO_CHOICES, default=6, blank=True)
    objects = ContentItemManager()

    @property
    def text_width(self):
        return self.ratio

    @property
    def image_width(self):
        return 12 - self.text_width

    class Meta:
        verbose_name = _('Picture + Text')
        verbose_name_plural = _('Picture + Text')

    def __str__(self):
        return Truncator(strip_tags(self.text)).words(20)

    def full_clean(self, *args, **kwargs):
        # This is called by the form when all values are assigned.
        # The pre filters are applied here, so any errors also appear as ValidationError.
        super(ImageTextItem, self).full_clean(*args, **kwargs)

        self.text, self.text_final = apply_filters(self, self.text, field_name='text')
        if self.text_final == self.text:
            # No need to store duplicate content:
            self.text_final = None


class Page(PublishableModel):
    """
    Slides for homepage.
    """

    class PageStatus(DjangoChoices):
        published = ChoiceItem('published', label=_('Published'))
        draft = ChoiceItem('draft', label=_('Draft'))

    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=False)
    full_page = models.BooleanField(
        _('Page without sub-navigation'),
        default=False,
        help_text=_('Show this page in full width and hide the sub-navigation')
    )

    # Contents
    language = models.CharField(
        _('language'),
        max_length=5,
        choices=lazy(get_languages, tuple)())
    body = PlaceholderField('blog_contents', plugins=[
        'TextPlugin',
        'ImageTextPlugin',
        'OEmbedPlugin',
        'RawHtmlPlugin',
        'PicturePlugin',
        'DocumentPlugin'
    ])
    # This should not be nessecary, but fixes deletion of some pages
    # See https://github.com/edoburu/django-fluent-contents/issues/19
    contentitem_set = ContentItemRelation()

    class Meta:
        ordering = ('language', 'slug')
        unique_together = ('language', 'slug')

        permissions = (
            ('api_read_page', 'Can view pages through the API'),
            ('api_add_page', 'Can add pages through the API'),
            ('api_change_page', 'Can change pages through the API'),
            ('api_delete_page', 'Can delete pages through the API'),
        )

    def __unicode__(self):
        return self.title

    def get_meta_description(self, **kwargs):
        request = kwargs.get('request')
        s = MLStripper()
        s.feed(mark_safe(render_placeholder(request, self.body).html))
        return truncatechars(s.get_data(), 200)
