"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
# Routers automatically create the URL patterns for us! Only used with viewsets!
# So we don't have to manually define them in our urls.py file
# We just need to register the viewset with the router and it will take care of the rest
# The first argument is the prefix, which is the URL that will be used to access the viewset
# The second argument is the viewset itself

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
