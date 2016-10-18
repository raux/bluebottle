from mock import patch

from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from bluebottle.tasks.models import Task
from bluebottle.test.utils import BluebottleTestCase
from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from bluebottle.test.factory_models.tasks import TaskFactory, TaskMemberFactory

from bluebottle.bb_projects.models import ProjectPhase
from bluebottle.analytics import signals
from bluebottle.analytics.backends import InfluxExporter
from .common import FakeInfluxDBClient

fake_client = FakeInfluxDBClient()


@override_settings(ANALYTICS_ENABLED=True)
@patch.object(signals, 'queue_analytics_record')
@patch.object(InfluxExporter, 'client', fake_client)
class TaskMemberApiAnalyticsTest(BluebottleTestCase):
    def setUp(self):
        super(TaskMemberApiAnalyticsTest, self).setUp()

        self.init_projects()

    def test_taskmember_status_changes(self, queue_mock):
        user = BlueBottleUserFactory.create()
        task = TaskFactory.create(author=user, people_needed=2, status='realized')
        task_member = TaskMemberFactory.create(time_spent=10, member=user, task=task, status='applied')

        task_member_url = reverse('task_member_detail', kwargs={'pk': task_member.id})
        task_member_data = {
            'task': task.id,
            'status': 'realized'
        }
        self.client.put(task_member_url, task_member_data, token="JWT {0}".format(user.get_jwt_token()))
        args, kwargs = queue_mock.call_args
        self.assertEqual(kwargs['tags']['status'], 'realized')

    def test_taskmember_delete_status_changes(self, queue_mock):
        user = BlueBottleUserFactory.create()
        task = TaskFactory.create(author=user, people_needed=2, status='realized')
        task_member = TaskMemberFactory.create(time_spent=10, member=user, task=task, status='applied')

        task_member_url = reverse('task_member_detail', kwargs={'pk': task_member.id})
        task_member_data = {
            'task': task.id,
            'status': 'withdrew'
        }
        self.client.put(task_member_url, task_member_data, token="JWT {0}".format(user.get_jwt_token()))
        args, kwargs = queue_mock.call_args
        self.assertEqual(kwargs['tags']['status'], 'withdrew')


@override_settings(ANALYTICS_ENABLED=True)
@patch.object(signals, 'queue_analytics_record')
@patch.object(InfluxExporter, 'client', fake_client)
class MemberApiAnalyticsTest(BluebottleTestCase):
    def setUp(self):
        super(MemberApiAnalyticsTest, self).setUp()

        def do_nothing(**kwargs):
            pass

        with patch('bluebottle.analytics.signals.queue_analytics_record') as mock_queue:
            mock_queue.side_effect = do_nothing
            self.user = BlueBottleUserFactory.create()

    def test_member_last_seen(self, queue_mock):
        profile_url = reverse('user-profile-detail', kwargs={'pk': self.user.id})
        self.client.get(profile_url, None, token="JWT {0}".format(self.user.get_jwt_token()))

        self.assertEqual(queue_mock.call_count, 1,
                         'Analytics should be called once when member accesses API')

        args, kwargs = queue_mock.call_args_list[0]
        self.assertEqual(kwargs['tags']['event'], 'seen',
                         'Analytics should be called with event = seen')

    @patch('bluebottle.auth.middleware.LAST_SEEN_DELTA', 10)
    def test_member_last_seen_inside_delta(self, queue_mock):
        profile_url = reverse('user-profile-detail', kwargs={'pk': self.user.id})
        self.client.get(profile_url, None, token="JWT {0}".format(self.user.get_jwt_token()))
        self.client.get(profile_url, None, token="JWT {0}".format(self.user.get_jwt_token()))

        self.assertEqual(queue_mock.call_count, 1,
                         'Analytics should not trigger event = seen if inside LAST_SEEN_DELTA')

    @patch('bluebottle.auth.middleware.LAST_SEEN_DELTA', 0)
    def test_member_last_seen_outside_delta(self, queue_mock):
        profile_url = reverse('user-profile-detail', kwargs={'pk': self.user.id})
        self.client.get(profile_url, None, token="JWT {0}".format(self.user.get_jwt_token()))
        self.client.get(profile_url, None, token="JWT {0}".format(self.user.get_jwt_token()))

        self.assertEqual(queue_mock.call_count, 2,
                         'Analytics should trigger event = seen if outside LAST_SEEN_DELTA')
