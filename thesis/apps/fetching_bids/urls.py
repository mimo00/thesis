from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter

from apps.fetching_bids.views import BidViewSet, auction_detail

router = SimpleRouter()
router.register(r"bids", BidViewSet, basename="bids")


urlpatterns = router.urls

urlpatterns += [
    url(r'^auction$', auction_detail, name='auction')
]

urlpatterns += [path("", RedirectView.as_view(url="/admin"))]
