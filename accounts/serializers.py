from rest_framework import serializers

from .models import Company, EmployeeProfile, RoleChoices, User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'slug', 'created_at')
        read_only_fields = ('id', 'created_at')


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ('start_date', 'department', 'position', 'mentor')


class UserSerializer(serializers.ModelSerializer):
    profile = EmployeeProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'company', 'profile', 'date_joined',
        )
        read_only_fields = ('id', 'date_joined', 'company')

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = EmployeeProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'profile',
        )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        company = self.context['request'].user.company
        user = User.objects.create_user(
            company=company,
            **validated_data,
        )
        if profile_data:
            EmployeeProfile.objects.create(user=user, **profile_data)
        return user


class RegisterCompanySerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    company_slug = serializers.SlugField(max_length=255)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, default='')
    last_name = serializers.CharField(max_length=150, required=False, default='')

    def create(self, validated_data):
        company = Company.objects.create(
            name=validated_data['company_name'],
            slug=validated_data['company_slug'],
        )
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            company=company,
            role=RoleChoices.ADMIN,
        )
        return user
