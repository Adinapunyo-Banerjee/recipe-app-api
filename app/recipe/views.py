"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()         # Objects available for use in the viewset
    authentication_classes = [TokenAuthentication]  # You need to use token auth to use this API view
    permission_classes = [IsAuthenticated]          # You also need to be authenticated to use this API view

    # Override the default queryset to only include recipes created by the current user
    def get_queryset(self):
        """Retrieve recipes for authenticated user ONLY!"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        # This function is called internally and by default returns self.serializer_class
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # Override behavior of saving a model to a viewset since we need to include the user creating the recipe.
        serializer.save(user=self.request.user)
