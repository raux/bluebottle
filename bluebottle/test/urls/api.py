from django.conf.urls import url

from ..views import ResourceList

urlpatterns = [
    url(r'^resource$', ResourceList.as_view(),
        name='resource-list'),
]
