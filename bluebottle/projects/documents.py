from django.db import connection

from django_elasticsearch_dsl import Index, DocType, fields, search
from elasticsearch_dsl import Q

from bluebottle.bb_projects.models import ProjectPhase
from bluebottle.geo.models import Location
from bluebottle.projects.models import Project
from bluebottle.utils.documents import MultiTenantIndex
from bluebottle.tasks.models import Task

# The name of your index
project = Index('projects')
# See Elasticsearch Indices API reference for available settings
project.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@project.doc_type
class ProjectDocument(DocType):
    client_name = fields.StringField()

    task_set = fields.NestedField(properties={
        'title': fields.StringField(),
        'description': fields.StringField(),
        'status': fields.StringField(),
        'deadline': fields.DateField(),
        'deadline_to_apply': fields.DateField(),
        'skill': fields.NestedField(
            properties={'name': fields.StringField()}
        ),
    })

    status = fields.ObjectField(properties={
        'slug': fields.StringField()
    })

    location = fields.ObjectField(properties={
        'id': fields.LongField(),
        'name': fields.StringField(),
        'position': fields.GeoPointField(),
        'city': fields.StringField()
    })

    country = fields.ObjectField(properties={
        'id': fields.LongField(),
        'name': fields.StringField(),
    })

    project_location = fields.GeoPointField()

    class Meta:
        model = Project
        fields = [
            'title',
            'story',
            'pitch',
            'popularity',
        ]
        related_models = (Task, ProjectPhase, Location)

    @classmethod
    def search(cls, using=None, index=None):
        return search.Search(
            using=using or cls._doc_type.using,
            index=index or cls._doc_type.index,
            doc_type=[cls],
            model=cls._doc_type.model
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Task):
            return related_instance.project
        elif isinstance(related_instance, ProjectPhase):
            return related_instance.project_set.all()
        elif isinstance(related_instance, Location):
            return related_instance.project_set.all()
        elif isinstance(related_instance, Country):
            return related_instance.project_set.all()


    def prepare_client_name(self, instance):
        return connection.tenant.client_name

    def prepare_project_location(self, instance):
        if instance.latitude and instance.longitude:
            return (instance.longitude, instance.latitude)
        else:
            return None
