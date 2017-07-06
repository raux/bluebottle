# flake8: noqa
import logging
from collections import defaultdict, namedtuple
from datetime import datetime
import pytz

import xlsxwriter
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Count, Sum
from django.utils import dateparse

from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant
from bluebottle.members.models import Member
from bluebottle.tasks.models import Task, TaskMember, TaskStatusLog, TaskMemberStatusLog
from bluebottle.projects.models import Project

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Export the DLL yearly metrics'

    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)

        self.tenants = []

        for client in Client.objects.all():
            self.tenants.append(client.client_name)

        self.year = None
        self.organisation = ''
        self.row_counter_raw_metric_data = 1
        self.time_periods = None
        self.raw_data = []
        self.Metric = namedtuple('Metric', 'name q1 q2 q3 q4')

    def add_arguments(self, parser):
        parser.add_argument('--year', metavar='YYYY', action='store', dest='year', required=True,
                            help="Calendar Year (YYYY) for metric generation")

        parser.add_argument('--tenants', metavar='TENANTS', action='store', dest='tenants', required=False, nargs='*',
                            choices=self.tenants, help="The names of the tenants to export")

    def handle(self, **options):
        self.tenants = set(options['tenants']) if options['tenants'] else None
        self.year = options['year']

        TimePeriod = namedtuple('TimePeriod', 'quarter start_date end_date')
        self.time_periods = [TimePeriod(quarter='Q1',
                                        start_date=dateparse.parse_datetime(
                                            '{}-01-01 00:00:00+00:00'.format(self.year)),
                                        end_date=dateparse.parse_datetime(
                                            '{}-03-31 23:59:59+00:00'.format(self.year))),
                             TimePeriod(quarter='Q2',
                                        start_date=dateparse.parse_datetime(
                                            '{}-01-01 00:00:00+00:00'.format(self.year)),
                                        end_date=dateparse.parse_datetime(
                                            '{}-06-30 23:59:59+00:00'.format(self.year))),
                             TimePeriod(quarter='Q3',
                                        start_date=dateparse.parse_datetime(
                                            '{}-01-01 00:00:00+00:00'.format(self.year)),
                                        end_date=dateparse.parse_datetime(
                                            '{}-09-30 23:59:59+00:00'.format(self.year))),
                             TimePeriod(quarter='Q4',
                                        start_date=dateparse.parse_datetime(
                                            '{}-01-01 00:00:00+00:00'.format(self.year)),
                                        end_date=dateparse.parse_datetime(
                                            '{}-12-31 23:59:59+00:00'.format(self.year))),
                             ]
        self.generate_metrics_xls()

    def generate_metrics_xls(self):
        file_name = self.get_xls_file_name(self.year)

        with xlsxwriter.Workbook(file_name) as workbook:
            for client in Client.objects.all():
                if self.tenants is None or client.client_name in self.tenants:
                    connection.set_tenant(client)
                    with LocalTenant(client, clear_tenant=True):
                        self.organisation = client.client_name
                        logger.info('export tenant:{}'.format(self.organisation))
                        self.generate_raw_data()
                        self.generate_raw_data_worksheet(workbook, self.raw_data)
                        # Reset raw data
                        self.raw_data = []

    @staticmethod
    def get_xls_file_name(year):
        return 'yearly_report_{}_generated_{}.xlsx'.format(year, datetime.now().strftime("%Y%m%d-%H%M%S"))

    @staticmethod
    def initialize_work_sheet(workbook, name, headers):
        worksheet = workbook.get_worksheet_by_name(name)
        if not worksheet:
            worksheet = workbook.add_worksheet(name)
            worksheet.write_row(0, 0, headers)
        return worksheet

    def generate_raw_data_worksheet(self, workbook, raw_data):
        metric_data_worksheet = self.initialize_metric_data_worksheet(workbook)
        self.write_metric_data(metric_data_worksheet, raw_data)
        return metric_data_worksheet

    def initialize_metric_data_worksheet(self, workbook):
        name = 'Yearly Results'
        headers = ('Metric', 'Organisation', 'Q1', 'Q2', 'Q3', 'Q4')
        return self.initialize_work_sheet(workbook, name, headers)

    def write_metric_data(self, worksheet, data):
        # List of named tuples
        # Metric = collections.namedtuple('Metric', 'name q1 q2 q3 q4')

        for metric in data:
            worksheet.write(self.row_counter_raw_metric_data, 0, metric.name)
            worksheet.write(self.row_counter_raw_metric_data, 1, self.organisation)
            worksheet.write(self.row_counter_raw_metric_data, 2, metric.q1)
            worksheet.write(self.row_counter_raw_metric_data, 3, metric.q2)
            worksheet.write(self.row_counter_raw_metric_data, 4, metric.q3)
            worksheet.write(self.row_counter_raw_metric_data, 5, metric.q4)

            self.row_counter_raw_metric_data += 1

    def generate_raw_data(self):
        self.generate_members_registered_data()
        self.generate_members_active_data()
        self.generate_tasks_submitted_data()
        self.generate_tasks_realized_data()
        self.generate_tasks_hours_data()
        self.generate_projects_submitted_data()
        self.generate_projects_initiated_data()
        self.generate_projects_realized_data()
        self.generate_project_initiators_data()
        self.generate_task_members_data()
        self.generate_task_hours_spent_data()

    def generate_members_registered_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                members_count = Member.objects \
                    .filter(date_joined__gte=time_period.start_date, date_joined__lte=time_period.end_date) \
                    .count()
                metrics['q{}'.format(quarter)] = members_count

        self.raw_data.append(self.Metric(name='Members Registered',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_members_active_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                project_initiators = Member.objects \
                    .filter(owner__created__gte=time_period.start_date,
                            owner__created__lte=time_period.end_date,
                            owner__status__slug__in=['voting', 'voting-done', 'campaign',
                                                     'to-be-continued', 'done-complete',
                                                     'done-incomplete']) \
                    .distinct('id') \
                    .values_list('id', flat=True)

                task_members = Member.objects \
                    .filter(
                tasks_taskmember_related__tasks_taskmemberstatuslog_related__start__gte=time_period.start_date,
                tasks_taskmember_related__tasks_taskmemberstatuslog_related__start__lte=time_period.end_date,
                tasks_taskmember_related__tasks_taskmemberstatuslog_related__status__in=['accepted', 'realized']) \
                    .distinct('id') \
                    .values_list('id', flat=True)

                metrics['q{}'.format(quarter)] = len(set(project_initiators) | set(task_members))

        self.raw_data.append(self.Metric(name='Members Active',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_tasks_submitted_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:

                tasks = Task.objects.\
                    filter(tasks_taskstatuslog_related__start__gte=time_period.start_date,
                           tasks_taskstatuslog_related__start__lte=time_period.end_date,
                           tasks_taskstatuslog_related__status__in=['open', 'in progress', 'realized']).\
                    order_by('id').\
                    distinct('id').\
                    values_list('id', flat=True)

                metrics['q{}'.format(quarter)] = len(tasks)

        self.raw_data.append(self.Metric(name='Activities Submitted',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_tasks_realized_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                tasks = Task.objects. \
                    filter(tasks_taskstatuslog_related__start__gte=time_period.start_date,
                           tasks_taskstatuslog_related__start__lte=time_period.end_date,
                           tasks_taskstatuslog_related__status='realized'). \
                    order_by('id'). \
                    distinct('id'). \
                    values_list('id', flat=True)

                metrics['q{}'.format(quarter)] = len(tasks)

        self.raw_data.append(self.Metric(name='Activities Realized',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_tasks_hours_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_time_spent = Member.objects \
                    .filter(tasks_taskmember_related__created__gte=time_period.start_date,
                            tasks_taskmember_related__created__lte=time_period.end_date,
                            tasks_taskmember_related__status='realized',
                            tasks_taskmember_related__time_spent__gt=0) \
                    .aggregate(Sum('tasks_taskmember_related__time_spent'))

                metrics['q{}'.format(quarter)] = total_time_spent['tasks_taskmember_related__time_spent__sum']

        self.raw_data.append(self.Metric(name='Activities Hours',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_projects_submitted_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_projects = Project.objects \
                    .filter(created__gte=time_period.start_date,
                            created__lte=time_period.end_date)\
                    .count()

                metrics['q{}'.format(quarter)] = total_projects

        self.raw_data.append(self.Metric(name='Projects Submitted',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_projects_initiated_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_projects = Project.objects \
                    .filter(created__gte=time_period.start_date,
                            created__lte=time_period.end_date,
                            status__slug__in=['plan-submitted',
                                            'plan-needs-work',
                                            'voting-done',
                                            'campaign',
                                            'done-incomplete',
                                            'plan-new',
                                            'voting',
                                            'to-be-continued',
                                            'done-complete'
                                            ])\
                    .count()

                metrics['q{}'.format(quarter)] = total_projects

        self.raw_data.append(self.Metric(name='Projects Initiated',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_projects_realized_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_projects = Project.objects \
                    .filter(created__gte=time_period.start_date,
                            created__lte=time_period.end_date,
                            status__slug__in=['done-incomplete','done-complete'])\
                    .count()

                metrics['q{}'.format(quarter)] = total_projects

        self.raw_data.append(self.Metric(name='Projects Realized',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_project_initiators_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                members = Member.objects \
                    .filter(owner__created__gte=time_period.start_date,
                            owner__created__lte=time_period.end_date) \
                    .distinct('id') \
                    .count()

                metrics['q{}'.format(quarter)] = members

        self.raw_data.append(self.Metric(name='Projects Initators',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))


    def generate_task_members_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                task_members = Member.objects \
                    .filter(
                tasks_taskmember_related__tasks_taskmemberstatuslog_related__start__gte=time_period.start_date,
                tasks_taskmember_related__tasks_taskmemberstatuslog_related__start__lte=time_period.end_date,
                tasks_taskmember_related__tasks_taskmemberstatuslog_related__status__in=['accepted', 'realized']) \
                    .distinct('id') \
                    .values_list('id', flat=True)

                metrics['q{}'.format(quarter)] = len(task_members)

        self.raw_data.append(self.Metric(name='Activity Members',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_task_hours_spent_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_time_spent = Member.objects \
                    .filter(tasks_taskmember_related__created__gte=time_period.start_date,
                            tasks_taskmember_related__created__lte=time_period.end_date,
                            tasks_taskmember_related__status='realized',
                            tasks_taskmember_related__time_spent__gt=0) \
                    .aggregate(Sum('tasks_taskmember_related__time_spent'))

                metrics['q{}'.format(quarter)] = total_time_spent['tasks_taskmember_related__time_spent__sum']

        self.raw_data.append(self.Metric(name='Hours Spent',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))
