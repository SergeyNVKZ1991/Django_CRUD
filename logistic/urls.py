from rest_framework.routers import DefaultRouter
from logistic.views import ProductViewSet, StockViewSet

router = DefaultRouter()
router.register('Проверка CI/CD', ProductViewSet)
router.register('stocks', StockViewSet)

urlpatterns = router.urls
