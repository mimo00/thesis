from rest_framework.routers import SimpleRouter

from apps.decisions.views import ChargingLocalizationDecisionViewSet

router = SimpleRouter()
router.register(r"charging-localization-decision", ChargingLocalizationDecisionViewSet,
                basename="point_schedule_decisions")


urlpatterns = router.urls
