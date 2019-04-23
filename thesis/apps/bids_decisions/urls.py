from rest_framework.routers import SimpleRouter

from apps.bids_decisions.views import BidDecisionViewSet

router = SimpleRouter()
router.register(r"bid-decisions", BidDecisionViewSet, basename="bid_decisions")


urlpatterns = router.urls
