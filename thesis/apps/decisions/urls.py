from rest_framework.routers import SimpleRouter

from apps.decisions.views import ChargingSchedulesDecisionViewSet

router = SimpleRouter()
router.register(r"charging-schedules-decisions", ChargingSchedulesDecisionViewSet,
                basename="charging_schedules_decision")


urlpatterns = router.urls
