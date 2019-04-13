from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.fetching_bids.views import BidViewSet

router = SimpleRouter()
router.register(r"bids", BidViewSet, basename="bids")


urlpatterns = router.urls
