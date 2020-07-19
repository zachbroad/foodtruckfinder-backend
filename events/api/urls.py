from .views import EventViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)