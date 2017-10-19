from datetime import timedelta
import factory

from django.utils.timezone import now

from bluebottle.cms.models import (
    ResultPage, Stats, Stat, Quotes, Quote, Projects,
    SiteLinks, LinkGroup, Link, LinkPermission
)
from bluebottle.test.factory_models.utils import LanguageFactory


class ResultPageFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = ResultPage

    title = factory.Sequence(lambda n: 'Result Page Title {0}'.format(n))
    slug = factory.Sequence(lambda n: 'slug-{0}'.format(n))
    description = factory.Sequence(lambda n: 'Results description {0}'.format(n))
    start_date = now() - timedelta(days=300)
    end_date = now() + timedelta(days=65)


class StatsFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Stats


class StatFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Stat

    type = 'manual'
    value = 500
    stats = factory.SubFactory(Stats)


class QuotesFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Quotes


class QuoteFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Quote

    name = factory.Sequence(lambda n: 'Name {}'.format(n))
    quote = factory.Sequence(lambda n: 'Quote {}'.format(n))
    quotes = factory.SubFactory(Quote)


class ProjectsFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Projects


class SiteLinksFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = SiteLinks

    language = factory.SubFactory(LanguageFactory)


class LinkGroupFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = LinkGroup
        django_get_or_create = ('name',)

    site_links = factory.SubFactory(SiteLinksFactory)
    name = factory.Sequence(lambda n: 'Link Group {}'.format(n))


class LinkFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Link

    link_group = factory.SubFactory(LinkGroupFactory)
    title = factory.Sequence(lambda n: 'Title {}'.format(n))


class LinkPermissionFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = LinkPermission
