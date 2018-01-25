from django.urls.base import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from jet.dashboard.modules import DashboardModule

from bluebottle.projects.models import Project
from bluebottle.tasks.models import Task


class RecentProjects(DashboardModule):
    title = _('Recently Submitted Projects')
    title_url = reverse('admin:projects_project_changelist')
    template = 'dashboard/recent_projects.html'
    limit = 10

    def init_with_context(self, context):
        self.children = Project.objects.filter(status__slug='plan-submitted').order_by('-created')[:self.limit]


class MyReviewingProjects(DashboardModule):
    title = _('Projects I\'m reviewing')
    title_url = reverse('admin:projects_project_changelist')
    template = 'dashboard/recent_projects.html'
    limit = 5

    def init_with_context(self, context):
        user = context.request.user
        self.children = Project.objects.filter(reviewer=user).order_by('-created')[:self.limit]


class ClosingFundingProjects(DashboardModule):
    title = _('Projects nearing deadline')
    title_url = reverse('admin:projects_project_changelist')
    template = 'dashboard/closing_funding_projects.html'
    limit = 5

    def init_with_context(self, context):
        self.children = Project.objects.filter(status__slug='campaign').order_by('deadline')[:self.limit]


class ClosingTasks(DashboardModule):
    title = _('Tasks nearing deadline')
    title_url = reverse('admin:tasks_task_changelist')
    template = 'dashboard/closing_tasks.html'
    limit = 5

    def init_with_context(self, context):
        tasks = Task.objects.exclude(deadline__lt=now()).filter(status__in=['open', 'full']).order_by('deadline')
        self.children = tasks[:self.limit]


class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(RecentProjects())
        self.children.append(MyReviewingProjects())
        self.children.append(ClosingFundingProjects())
        self.children.append(ClosingTasks())

        self.children.append(modules.LinkList(
            _('Some links'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))

        self.children.append(modules.LinkList(
            _('More links'),
            children=[
                {
                    'title': _('Interwebs'),
                    'url': 'http://interwebs.com/',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))