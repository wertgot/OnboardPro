from datetime import date

from django.core.management.base import BaseCommand

from accounts.models import Company, EmployeeProfile, RoleChoices, User
from instances.models import OnboardingInstance
from instances.services import create_instance_progress, recalculate_progress
from programs.models import OnboardingProgram, OnboardingStage, Task


class Command(BaseCommand):
    help = 'Создаёт демо-данные для тестирования API'

    def handle(self, *args, **options):
        company, _ = Company.objects.get_or_create(
            slug='demo', defaults={'name': 'Demo Company'}
        )
        def ensure_user(username, email, role, first_name, last_name):
            user = User.objects.filter(username=username).first()
            if user is None:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='demo1234',
                    company=company,
                    role=role,
                    first_name=first_name,
                    last_name=last_name,
                )
            elif not user.check_password('demo1234'):
                user.set_password('demo1234')
                user.save(update_fields=['password'])
            return user

        admin = ensure_user(
            'admin@demo.com', 'admin@demo.com', RoleChoices.ADMIN, 'Админ', 'Демо'
        )
        hr = ensure_user(
            'hr@company.com', 'hr@company.com', RoleChoices.HR, 'HR', 'Менеджер'
        )
        emp = ensure_user(
            'employee@company.com', 'employee@company.com',
            RoleChoices.EMPLOYEE, 'Иван', 'Петров',
        )

        EmployeeProfile.objects.get_or_create(
            user=emp,
            defaults={
                'start_date': date(2025, 1, 15),
                'department': 'IT',
                'position': 'Junior Developer',
                'mentor': hr,
            },
        )

        program, _ = OnboardingProgram.objects.get_or_create(
            company=company,
            name='IT-онбординг',
            defaults={'description': 'Программа адаптации для IT-отдела'},
        )
        if not program.stages.exists():
            s1 = OnboardingStage.objects.create(program=program, name='День 1', order=1)
            s2 = OnboardingStage.objects.create(program=program, name='Неделя 1', order=2)
            Task.objects.create(
                stage=s1, title='Ознакомление с политикой', task_type='info',
                due_days=1, content='Прочитайте корпоративную политику.',
            )
            Task.objects.create(
                stage=s1, title='Подписать NDA', task_type='document', due_days=3,
            )
            Task.objects.create(
                stage=s2, title='Настройка рабочего места', task_type='checklist', due_days=7,
            )

        if not OnboardingInstance.objects.filter(employee=emp, program=program).exists():
            instance = OnboardingInstance.objects.create(employee=emp, program=program)
            create_instance_progress(instance)
            recalculate_progress(instance)

        self.stdout.write(self.style.SUCCESS('Демо-данные готовы.'))
        self.stdout.write('  hr@company.com / demo1234')
        self.stdout.write('  employee@company.com / demo1234')
        self.stdout.write('  admin@demo.com / demo1234')
