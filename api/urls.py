from django.urls import path, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'infos', views.InfoViewSet)
router.register(r'containers', views.ContainerViewSet)
router.register(r'persons', views.PersonViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("", include(router.urls)),
    path('get-token/', views.CustomAuthToken.as_view()),
    path('history/by-person/', views.ListHistoryByPersonView.as_view()),
    path('history/by-date/', views.ListHistoryByPersonByDateView.as_view()),
    path('calculate/daily-goal/', views.CalcDailyGoalView.as_view()),
    path('calculate/remaining-goal/', views.CalcRemainingGoalView.as_view()),
    path('calculate/remaining-percentage/',
         views.CalcRemainingPercentGoalView.as_view()),
    path('drink/', views.ConsumeDrinkView.as_view()),
]
