from django.conf.urls import url

from ..views import PageDetail, PageList, PageDraftDetail

urlpatterns = [
    url(r'^$',
        PageList.as_view(),
        name='cms-page-list'),

    url(r'^(?P<pk>\d+)$',
        PageDetail.as_view(),
        name='cms-page-detail'),

    url(r'^preview/(?P<pk>\d+)$',
        PageDraftDetail.as_view(),
        name='cms-page-preview-detail'),
]
