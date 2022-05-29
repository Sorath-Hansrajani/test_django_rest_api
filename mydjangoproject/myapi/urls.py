"""from django.urls import path
from .views import PersonViewSet

urlpatterns = [
    path('persons/', PersonViewSet.person_list),
    path('persons/<int:id>/', PersonViewSet.person_by_id),
]"""

from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

#router = routers.DefaultRouter()
#router.register(r'persons', views.PersonViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('persons/', views.person_list),
    #path('persons/<int:id>/', views.person_by_id),
]

urlpatterns = format_suffix_patterns(urlpatterns)
