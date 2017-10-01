# flake8: noqa
import logging
from collections import defaultdict, namedtuple, Counter
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
    help = 'Export the yearly metrics'

    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)

        self.tenants = []

        for client in Client.objects.all():
            self.tenants.append(client.client_name)

        self.year = None
        self.organisation = ''

        self.row_counter_metric_data = 1
        self.row_counter_segmented_data = 1

        self.time_periods = None

        self.raw_data = []
        self.segmented_data = []

        self.Metric = namedtuple('Metric', 'name q1 q2 q3 q4')
        self.LocationMetric = namedtuple('LocationMetric', 'name quarter location_type location_name')

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
                        # self.generate_metric_data()
                        # self.generate_metric_data_worksheet(workbook, self.raw_data)

                        segmented_data = self.generate_segmented_data()
                        self.generate_segmented_data_worksheet(workbook, segmented_data)

                        # Reset data
                        self.raw_data = []
                        self.segmented_data = []

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

    def generate_metric_data_worksheet(self, workbook, raw_data):
        worksheet = self.initialize_metric_data_worksheet(workbook)
        self.write_metric_data(worksheet, raw_data)
        return worksheet


    def generate_segmented_data_worksheet(self, workbook, raw_data):
        worksheet = self.initialize_segmented_data_worksheet(workbook)
        self.write_segmented_data(worksheet, raw_data)
        return worksheet

    def initialize_metric_data_worksheet(self, workbook):
        name = 'Yearly Results'
        headers = ('Metric', 'Organisation', 'Q1', 'Q2', 'Q3', 'Q4')
        return self.initialize_work_sheet(workbook, name, headers)

    def initialize_segmented_data_worksheet(self, workbook):
        name = 'Segmented Results'
        headers = ('Metric', 'Quarter', 'Country', 'City', 'Total')
        return self.initialize_work_sheet(workbook, name, headers)

    def write_metric_data(self, worksheet, data):
        # List of named tuples
        # Metric = collections.namedtuple('Metric', 'name q1 q2 q3 q4')

        for metric in data:
            worksheet.write(self.row_counter_metric_data, 0, metric.name)
            worksheet.write(self.row_counter_metric_data, 1, metric.quarter)
            worksheet.write(self.row_counter_metric_data, 2, metric.q1)
            worksheet.write(self.row_counter_metric_data, 3, metric.q2)
            worksheet.write(self.row_counter_metric_data, 4, metric.q3)
            worksheet.write(self.row_counter_metric_data, 5, metric.q4)

            self.row_counter_metric_data += 1

    def write_segmented_data(self, worksheet, data):
        # List of named tuples
        # namedtuple('LocationMetric', 'name quarter location_country location_city total')

        for metric in data:
            worksheet.write(self.row_counter_metric_data, 0, metric.name)
            worksheet.write(self.row_counter_metric_data, 1, metric.quarter)
            worksheet.write(self.row_counter_metric_data, 2, metric.location_country)
            worksheet.write(self.row_counter_metric_data, 3, metric.location_city)
            worksheet.write(self.row_counter_metric_data, 4, metric.total)

            self.row_counter_metric_data += 1

    def generate_metric_data(self):

        # self.generate_unique_members()
        # self.generate_members_registered_data()
        # self.generate_members_active_data()
        # self.generate_tasks_submitted_data()
        # self.generate_tasks_realized_data()
        # self.generate_tasks_hours_data()
        # self.generate_projects_submitted_data()
        # self.generate_projects_initiated_data()
        # self.generate_projects_realized_data()
        # self.generate_project_initiators_data()
        # self.generate_task_members_data()
        # self.generate_task_hours_spent_data()
        pass

    def generate_members_registered_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                members_count = Member.objects \
                    .filter(date_joined__gte=time_period.start_date,
                            date_joined__lte=time_period.end_date) \
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
                            owner__status__slug__in=['voting',
                                                     'voting-done',
                                                     'campaign',
                                                     'to-be-continued',
                                                     'done-complete',
                                                     'done-incomplete']) \
                    .distinct('id') \
                    .values_list('id', flat=True)

                task_members = Member.objects \
                    .filter(tasks_taskmember_related__created__gte=time_period.start_date,
                            tasks_taskmember_related__created__lte=time_period.end_date,
                            tasks_taskmember_related__status__in=['accepted', 'realized']) \
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

                tasks = Task.objects\
                    .filter(created__gte=time_period.start_date,
                           created__lte=time_period.end_date,
                           status__in=['open',
                                       'in progress',
                                       'realized'])\
                    .count()

                metrics['q{}'.format(quarter)] = tasks

        self.raw_data.append(self.Metric(name='Activities Submitted',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_tasks_realized_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                tasks = Task.objects\
                    .filter(created__gte=time_period.start_date,
                           created__lte=time_period.end_date,
                           status='realized')\
                    .count()

                metrics['q{}'.format(quarter)] = tasks

        self.raw_data.append(self.Metric(name='Activities Realized',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_tasks_hours_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_time_spent = Member.objects\
                    .filter(tasks_taskmember_related__created__gte=time_period.start_date,
                            tasks_taskmember_related__created__lte=time_period.end_date,
                            tasks_taskmember_related__status='realized',
                            tasks_taskmember_related__time_spent__gt=0)\
                    .aggregate(total_hours=Sum('tasks_taskmember_related__time_spent'))

                metrics['q{}'.format(quarter)] = total_time_spent['total_hours']

        self.raw_data.append(self.Metric(name='Activities Hours',
                                         q1=metrics['q1'],
                                         q2=metrics['q2'],
                                         q3=metrics['q3'],
                                         q4=metrics['q4']))

    def generate_projects_submitted_data(self):
        metrics = defaultdict(lambda: '')
        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:
                total_projects = Project.objects\
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
                total_projects = Project.objects\
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
                total_projects = Project.objects\
                    .filter(created__gte=time_period.start_date,
                            created__lte=time_period.end_date,
                            status__slug__in=['done-incomplete',
                                              'done-complete'])\
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
                members = Member.objects\
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
                task_members = Member.objects\
                    .filter(tasks_taskmember_related__tasks_taskmemberstatuslog_related__start__gte=time_period.start_date,
                            tasks_taskmember_related__tasks_taskmemberstatuslog_related__start__lte=time_period.end_date,
                            tasks_taskmember_related__tasks_taskmemberstatuslog_related__status__in=['accepted', 'realized']) \
                    .distinct('id')\
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
    @staticmethod
    def get_country_name(location):
        if location.country:
            return location.country.name
        else:
            return '-'


    def generate_segmented_data(self):

        LocationMetric = namedtuple('LocationMetric', 'name quarter location_country location_city total')

        metrics_location = []

        # total_members = Member.objects.count()
        # print('Total Members: {}'.format(total_members))
        #

        for quarter, time_period in enumerate(self.time_periods, start=1):
            if datetime.utcnow().replace(tzinfo=pytz.utc) >= time_period.end_date:


                # Number of realized projects global/per country

                # total_projects = Project.objects \
                #     .filter(created__gte=time_period.start_date,
                #             created__lte=time_period.end_date,
                #             status__slug__in=['done-incomplete',
                #                               'done-complete'])
                # print('Total Projects Realized till end of Q{}: {}'.format(quarter, len(total_projects)))

                projects_per_country = Project.objects \
                                            .filter(created__gte=time_period.start_date,
                                                    created__lte=time_period.end_date,
                                                    status__slug__in=['done-incomplete',
                                                                      'done-complete'])\
                                            .values('location__country__name', 'location__city')\
                                            .annotate(total=Count('id'))\
                                            .order_by('total')

                for data in projects_per_country:
                    metrics_location.append(LocationMetric(name='Realized Projects',
                                                           quarter='Q{}'.format(quarter),
                                                           location_country=data['location__country__name'],
                                                           location_city=data['location__city'],
                                                           total=data['total']))


                # Number of realized participants global/ per country

                # total_realized_task_members = TaskMember.objects\
                #                         .filter(created__gte=time_period.start_date,
                #                                 created__lte=time_period.end_date,
                #                                 status='realized')\
                #                         .count()
                # print('Realized participants till end of Q{}: {}'.format(quarter, total_realized_task_members))

                locations = defaultdict(set)
                realized_task_members = TaskMember.objects \
                                                .filter(task__deadline__gte=time_period.start_date,
                                                        task__deadline__lte=time_period.end_date,
                                                        status='realized')

                for task_member in realized_task_members:
                    locations[u'{}__{}'.format(self.get_country_name(task_member.project.location),
                                               task_member.project.location.city)].add(task_member.id)

                for location, members in locations.iteritems():
                    country, city = location.split('__')
                    metrics_location.append(LocationMetric(name='Unique Realized Participants',
                                                           quarter='Q{}'.format(quarter),
                                                           location_country=country,
                                                           location_city=city,
                                                           total=len(members)))


                # Number of hours realized global/Per country

                # total_realized_hours = realized_task_members.aggregate(total_hours=Sum('time_spent'))
                # print('Realized Hours till end of Q{}: {}'.format(quarter, total_realized_hours))

                total_realized_hours_by_location = defaultdict(int)
                for task_member in realized_task_members:
                    total_realized_hours_by_location[u'{}__{}'
                        .format(self.get_country_name(task_member.project.location),
                                task_member.project.location.city)] += task_member.time_spent

                for location, total in total_realized_hours_by_location.iteritems():
                    country, city = location.split('__')
                    metrics_location.append(LocationMetric(name='Realized Hours',
                                                           quarter='Q{}'.format(quarter),
                                                           location_country=country,
                                                           location_city=city,
                                                           total=total))

                # Number of unique members global/per country
                location_members = defaultdict(list)
                projects = Project.objects.filter(created__gte=time_period.start_date,
                                                  created__lte=time_period.end_date,
                                                  status__slug__in=['voting',
                                                                    'voting-done',
                                                                    'campaign',
                                                                    'done-complete',
                                                                    'done-incomplete'])

                for project in projects:
                    location_members[u'{}__{}'.format(self.get_country_name(project.location), project.location.city)].append(project.owner.id)

                    task_members = TaskMember.objects.filter(task__project=project)

                    for task_member in task_members:
                        location_members[u'{}__{}'.format(self.get_country_name(project.location), project.location.city)].append(task_member.id)

                for location, members in location_members.iteritems():
                    country, city = location.split('__')
                    metrics_location.append(LocationMetric(name='Unique Members',
                                                           quarter='Q{}'.format(quarter),
                                                           location_country=country,
                                                           location_city=city,
                                                           total=len(set(members))))
        return metrics_location
