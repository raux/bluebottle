# Create csv export for projects, members, donations, votes, pages, comments
import csv
import sys

from django.test import RequestFactory
from django.utils import translation

from fluent_contents.rendering import render_placeholder

from bluebottle.clients.utils import LocalTenant
from bluebottle.clients.models import Client
from bluebottle.projects.models import Project
from bluebottle.members.models import Member
from bluebottle.news.models import NewsItem
from bluebottle.donations.models import Donation
from bluebottle.votes.models import Vote
from bluebottle.pages.models import Page
from bluebottle.wallposts.models import Wallpost


def get_field(obj, field):
    if field.startswith('rendered_') == 'rendered_content':
        return render_placeholder(
            RequestFactory().get('/test'),
            getattr(obj, field.split('_')[-1])
        )

    bits = field.split('__')
    for bit in bits:
        obj = getattr(obj, bit, None)

        if obj is None:
            return ""

    return unicode(obj).encode('utf-8')


def get_data(qs, fields):
    for obj in qs.iterator():
        yield [get_field(obj, field) for field in fields]


def create_csv(qs, fields, filename):
    data = get_data(qs, fields)
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for row in data:
            writer.writerow(row)


def run(schema_name):
    translation.activate('en')
    with LocalTenant(
        Client.objects.get(schema_name=schema_name),
        clear_tenant=True
    ):
        fields = (
            'id', 'title', 'owner__email', 'pitch', 'theme', 'deadline', 'description',
            'country', 'amount_asked', 'story', 'campaign_started', 'campaign_ended', 'place',
        )
        create_csv(
            Project.objects.select_related('owner'),
            fields,
            'projects.csv'
        )

        fields = ('email', 'date_joined', 'first_name', 'last_name', 'place', 'about_me', 'last_seen')
        create_csv(Member.objects.all(), fields, 'members.csv')

        fields = ('amount', 'project', 'create', 'order__status', 'amount')
        create_csv(Donation.objects.all(), fields, 'donations.csv')

        fields = ('title', 'publication_date', 'status', 'rendered_contents')
        create_csv(NewsItem.objects.all(), fields, 'news.csv')

        fields = ('author__email', 'created', 'text', 'content_type', 'content_obj')
        create_csv(Wallpost.objects.all(), fields, 'wallposts.csv')

        fields = ('title', 'publication_date', 'status', 'rendered_body')
        create_csv(Page.objects.all(), fields, 'pages.csv')

        fields = ('created', 'project', 'voter__email', 'ip_address')
        create_csv(
            Vote.objects.select_related('voter', 'project'),
            fields,
            'votes.csv'
        )
