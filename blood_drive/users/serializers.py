from rest_framework import serializers
from .models import CustomUser, DonorProfile

class DonorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorProfile
        fields = ['dob', 'phone_number', 'blood_type', 'last_donation_date']

class UserSerializer(serializers.ModelSerializer):
    donor_profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'donor_profile']

    def get_donor_profile(self, obj):
        if obj.role == 'donor' and hasattr(obj, 'donor_profile'):
            return DonorProfileSerializer(obj.donor_profile).data
        return None

class RegisterSerializer(serializers.ModelSerializer):
    donor_profile = DonorProfileSerializer(required=False)  # optional in registration
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'donor_profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('donor_profile', None)
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        # create donor profile only if role is donor and profile data exists
        if user.role == 'donor':
            if profile_data:
                DonorProfile.objects.create(user=user, **profile_data)
            else:
                DonorProfile.objects.create(user=user)  # create empty profile

        return user
