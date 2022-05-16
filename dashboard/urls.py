from rest_framework import routers
from .views import (
    ExcelViewsets,
)

router = routers.SimpleRouter()
router.register(r'dataset', ExcelViewsets)

urlpatterns = router.urls