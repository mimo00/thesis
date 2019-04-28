from rest_framework.routers import SimpleRouter

from apps.bids_decisions.views import ChargingLocalizationDecisionViewSet

router = SimpleRouter()
router.register(r"charging-localization-decision", ChargingLocalizationDecisionViewSet,
                basename="charging_localization_decisions")


urlpatterns = router.urls
