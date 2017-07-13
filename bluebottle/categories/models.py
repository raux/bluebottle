from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from bluebottle.clients import properties
from bluebottle.utils.fields import ImageField


class Category(models.Model):
    title = models.CharField(_("name"), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_("description"))
    image = ImageField(_("image"), max_length=255, blank=True, null=True, upload_to='categories/',
                       help_text=_("Category image"))
    image_logo = ImageField(_("logo"), max_length=255, blank=True, null=True, upload_to='categories/logos/',
                            help_text=_("Category Logo image"))

    @property
    def projects(self):
        return self.project_set\
            .order_by('-favorite', '-popularity')\
            .filter(status__slug__in=['campaign', 'done-complete', 'done-incomplete', 'voting', 'voting-done'])

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(**kwargs)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return 'https://{}/projects/?category={}'.format(properties.tenant.domain_url, self.slug)


class CategoryContent(models.Model):
    category = models.ForeignKey(Category, related_name='contents')
    title = models.CharField(_('title'), max_length=60)
    description = models.TextField(_("description"), max_length=190)
    image = ImageField(_("image"), max_length=255, blank=True, null=True, upload_to='categories/content/',
                       help_text=_("Category content image"))
    video_url = models.URLField(max_length=100, blank=True, default='')
    link = models.URLField(_('Link url'), blank=True)

    class Meta:
        verbose_name = _("category content")
        verbose_name_plural = _("category contents")

    def __unicode__(self):
        return self.title
