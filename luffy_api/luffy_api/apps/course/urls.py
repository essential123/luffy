from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register('category', views.CourseCategoryView, 'category')
router.register('list', views.CourseView, 'list')
router.register('chapter', views.CourseChapterView, 'chapter')
router.register('search', views.CourseSearchView, 'search')
# router.register('pay', views.PayView, 'pay')

urlpatterns = [
]
urlpatterns += router.urls
