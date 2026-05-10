"""
Serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        # What model does the serializer represent?
        model = get_user_model()
        fields = ['email', 'password', 'name']  # Info to serialize and deserialize. Model constraints pulled automatically
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # This method overrides the default behavior of the ModelSerializer's create() method
        # We do this because the UserManager.create_user() method is used to create a user with an encrypted password,
        # and we want to use that same logic here instead of saving the password as plaintext by default.
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        # This method overrides the default behavior of the ModelSerializer's update() method.
        # We do this to not save the password as plaintext in the database!
        password = validated_data.pop('password', None)  # Get and remove the password from the dictionary!
        user = super().update(instance, validated_data)  # Call the superclass's update method to update everything else OTHER than the password!
        if password:  # Now we check if a new password was indeed set.
            user.set_password(password)  # Set the new password using set_password() method which encrypts it.
            user.save()  # Save the updated user object to persist the changes.
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # If everything checks out, return the authenticated user's token.
        attrs['user'] = user
        return attrs

