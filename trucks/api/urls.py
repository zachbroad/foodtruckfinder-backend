
from .views import MenuItemViewSet, ReviewsViewSet, VisitViewSet, TagsViewSet, LiveViewSet, TruckViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'menu items', MenuItemViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'lives', LiveViewSet)

urlpatterns = [
    # path('/', TruckListView.as_view(), name='truck-create'),
    # path('<int:pk>/', TruckDetailView.as_view(), name='truck-rud'),
    # path('<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-rud')
]

