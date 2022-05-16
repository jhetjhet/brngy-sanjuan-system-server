from rest_framework import routers
from .views import AuthenticationLogsViewsets

router = routers.SimpleRouter()
router.register(r'logs', AuthenticationLogsViewsets)

urlpatterns = router.urls