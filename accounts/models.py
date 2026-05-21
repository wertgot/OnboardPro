from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    HR = 'hr', 'HR-менеджер'
    EMPLOYEE = 'employee', 'Сотрудник'


class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='users'
    )
    role = models.CharField(max_length=20, choices=RoleChoices.choices)

    def __str__(self):
        return self.get_full_name() or self.username


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    start_date = models.DateField()
    mentor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='mentees'
    )
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} — {self.position}'
