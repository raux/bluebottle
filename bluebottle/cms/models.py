from django.db import models
from django.utils.translation import ugettext_lazy as _

from fluent_contents.models import PlaceholderField, ContentItem

from parler.models import TranslatableModel, TranslatedFields

from bluebottle.surveys.models import Survey
from bluebottle.projects.models import Project
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

from bluebottle.tasks.models import Task


class ResultPage(TranslatableModel):
    image = models.ImageField(_('Header image'), blank=True, null=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    content = PlaceholderField('content', plugins=[
        'MetricsBlockPlugin',
        'ProjectImagesBlockPlugin',
        'ProjectMapBlockPlugin',
        'ProjectsBlockPlugin',
        'QuotesBlockPlugin',
        'ShareResultsBlockPlugin',
        'SurveyBlockPlugin',
        'TasksBlockPlugin',

        # Phase out
        'StatsBlockPlugin',
    ])

    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=40),
        slug=models.SlugField(_('Slug'), max_length=40),
        description=models.CharField(_('Description'), max_length=45, blank=True, null=True)
    )

    class Meta:
        permissions = (
            ('api_read_resultpage', 'Can view result pages through the API'),
            ('api_add_resultpage', 'Can add result pages through the API'),
            ('api_change_resultpage', 'Can change result pages through the API'),
            ('api_delete_resultpage', 'Can delete result pages through the API'),
        )


class Stats(models.Model):
    def __unicode__(self):
        return u"List of statistics #{0}".format(self.id)


class Stat(TranslatableModel, SortableMixin):
    STAT_CHOICES = [
        ('manual', _('Manual input')),
        ('people_involved', _('People involved')),
        ('participants', _('Participants')),
        ('projects_realized', _('Projects realised')),
        ('projects_complete', _('Projects complete')),
        ('tasks_realized', _('Tasks realised')),
        ('task_members', _('Taskmembers')),
        ('donated_total', _('Donated total')),
        ('pledged_total', _('Pledged total')),
        ('amount_matched', _('Amount matched')),
        ('projects_online', _('Projects Online')),
        ('votes_cast', _('Votes casts')),
        ('time_spent', _('Time spent')),
    ]

    type = models.CharField(
        max_length=25,
        choices=STAT_CHOICES
    )
    value = models.CharField(max_length=63, null=True, blank=True,
                             help_text=_('Use this for \'manual\' input or the override the calculated value.'))
    stats = SortableForeignKey(Stats)
    sequence = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=63)
    )

    @property
    def name(self):
        return self.title

    class Meta:
        ordering = ['sequence']


class Metric(TranslatableModel, SortableMixin):
    STAT_CHOICES = [
        ('manual', _('Manual input')),
        ('people_involved', _('People involved')),
        ('participants', _('Participants')),
        ('projects_realized', _('Projects realised')),
        ('projects_complete', _('Projects complete')),
        ('tasks_realized', _('Tasks realised')),
        ('task_members', _('Taskmembers')),
        ('donated_total', _('Donated total')),
        ('pledged_total', _('Pledged total')),
        ('amount_matched', _('Amount matched')),
        ('projects_online', _('Projects Online')),
        ('votes_cast', _('Votes casts')),
        ('time_spent', _('Time spent')),
    ]

    type = models.CharField(
        max_length=25,
        choices=STAT_CHOICES
    )
    value = models.CharField(max_length=63, null=True, blank=True,
                             help_text=_('Use this for \'manual\' input or the override the calculated value.'))

    sequence = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    block = SortableForeignKey('cms.MetricsContent', related_name='metrics')

    translations = TranslatedFields(
        title=models.CharField(max_length=63)
    )

    @property
    def name(self):
        return self.title

    class Meta:
        ordering = ['sequence']


class Quote(TranslatableModel):
    block = models.ForeignKey('cms.QuotesContent', related_name='quotes')
    translations = TranslatedFields(
        name=models.CharField(max_length=30),
        quote=models.CharField(max_length=60)
    )


class ResultsContent(ContentItem):
    title = models.CharField(max_length=40, blank=True, null=True)
    sub_title = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        abstract = True


class QuotesContent(ResultsContent):
    type = 'quotes'
    preview_template = 'admin/cms/preview/quotes.html'

    class Meta:
        verbose_name = _('Quotes')

    def __unicode__(self):
        return unicode(self.quotes)


class StatsContent(ResultsContent):
    type = 'statistics'
    stats = models.ForeignKey(Stats)
    preview_template = 'admin/cms/preview/stats.html'

    class Meta:
        verbose_name = _('Platform Statistics')

    def __unicode__(self):
        return unicode(self.stats)


class SurveyContent(ResultsContent):
    type = 'survey'
    preview_template = 'admin/cms/preview/results.html'
    survey = models.ForeignKey(Survey, null=True)

    class Meta:
        verbose_name = _('Platform Results')

    def __unicode__(self):
        return unicode(self.survey)


class Projects(models.Model):
    projects = models.ManyToManyField(Project)

    def __unicode__(self):
        return u"List of projects #{0}".format(self.id)


class ProjectsContent(ResultsContent):
    action_text = models.CharField(max_length=40,
                                   default=_('Start your own project'),
                                   blank=True, null=True)
    action_link = models.CharField(max_length=100, default="/start-project",
                                   blank=True, null=True)

    projects = models.ForeignKey(Projects, null=True)

    type = 'projects'
    preview_template = 'admin/cms/preview/projects.html'

    class Meta:
        verbose_name = _('Projects')

    def __unicode__(self):
        return unicode(self.projects)


class ProjectImagesContent(ResultsContent):
    type = 'project_images'
    preview_template = 'admin/cms/preview/project_images.html'

    description = models.TextField(max_length=70, blank=True, null=True)
    action_text = models.CharField(max_length=40,
                                   default=_('Check out our projects'),
                                   blank=True, null=True)
    action_link = models.CharField(max_length=100, default="/projects?status=campaign%2Cvoting ",
                                   blank=True, null=True)

    class Meta:
        verbose_name = _('Project Images')

    def __unicode__(self):
        return 'Project images block'


class ShareResultsContent(ResultsContent):
    type = 'share-results'
    preview_template = 'admin/cms/preview/share_results.html'

    share_title = models.CharField(max_length=100, default='')
    share_text = models.CharField(
        max_length=100,
        default='',
        help_text="{amount}, {projects}, {tasks}, {hours}, {votes}, {people} will be replaced by live statistics"
    )

    class Meta:
        verbose_name = _('Share Results')

    def __unicode__(self):
        return 'Share results block'


class TasksContent(ResultsContent):
    type = 'tasks'
    preview_template = 'admin/cms/preview/tasks.html'
    action_text = models.CharField(max_length=40, blank=True, null=True)
    action_link = models.CharField(max_length=100, blank=True, null=True)

    tasks = models.ManyToManyField(Task, db_table='cms_taskscontent_tasks')

    class Meta:
        verbose_name = _('Tasks')

    def __unicode__(self):
        return 'Tasks'


class MetricsContent(ResultsContent):
    type = 'statistics'
    preview_template = 'admin/cms/preview/metrics.html'

    class Meta:
        verbose_name = _('Metrics')

    def __unicode__(self):
        return 'Metrics'


class ProjectsMapContent(ResultsContent):
    type = 'projects-map'
    preview_template = 'admin/cms/preview/projects_map.html'

    class Meta:
        verbose_name = _('Projects Map')

    def __unicode__(self):
        return 'Projects Map'


class SupporterTotalContent(ResultsContent):
    type = 'supporter_total'
    preview_template = 'admin/cms/preview/supporter_total.html'

    co_financer_title = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        verbose_name = _('Supporter total')

    def __unicode__(self):
        return 'Supporter total'
