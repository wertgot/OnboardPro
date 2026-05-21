from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from onboardpro.permissions import IsAdmin, IsHR

from .models import RoleChoices, User
from .serializers import (
    RegisterCompanySerializer,
    UserCreateSerializer,
    UserSerializer,
)


class RegisterCompanyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'id': user.id, 'username': user.username, 'company_id': user.company_id},
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = User.objects.filter(company=self.request.user.company).select_related(
            'company', 'profile'
        )
        if self.request.user.role == RoleChoices.EMPLOYEE:
            return qs.filter(pk=self.request.user.pk)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update', 'partial_update'):
            return [IsAdmin()]
        if self.action in ('list', 'retrieve'):
            if self.request.user.role == RoleChoices.EMPLOYEE:
                return [IsAuthenticated()]
            return [IsHR()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
