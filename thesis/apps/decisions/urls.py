from rest_framework.routers import SimpleRouter

from apps.decisions.views import SchedulesDecisionViewSet

router = SimpleRouter()
router.register(r"charging-schedules-decisions", SchedulesDecisionViewSet,
                basename="charging_schedules_decision")


urlpatterns = router.urls
