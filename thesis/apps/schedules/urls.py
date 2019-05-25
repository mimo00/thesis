from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter

from apps.schedules.views import ScheduleViewSet, auction_detail, TriggerAggregationView

router = SimpleRouter()
router.register(r"charging-schedules", ScheduleViewSet, basename="charging-schedules")


urlpatterns = router.urls

urlpatterns += [
    url(r'^auction$', auction_detail, name='auction'),
    url(r'^trigger-aggregation', TriggerAggregationView.as_view(), name='trigger_aggregation')
]

urlpatterns += [path("", RedirectView.as_view(url="/admin"))]
