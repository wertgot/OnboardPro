from django.db.models import Avg, Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from instances.models import OnboardingInstance
from onboardpro.permissions import IsHR
from programs.models import OnboardingProgram


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated, IsHR]

    def get(self, request):
        company = request.user.company
        instances = OnboardingInstance.objects.filter(program__company=company)

        by_status = dict(
            instances.values('status').annotate(count=Count('id')).values_list('status', 'count')
        )
        programs = OnboardingProgram.objects.filter(company=company).annotate(
            instance_count=Count('instances'),
            active_count=Count('instances', filter=Q(instances__status='in_progress')),
        )
        program_stats = [
            {
                'id': p.id,
                'name': p.name,
                'instance_count': p.instance_count,
                'active_count': p.active_count,
            }
            for p in programs
        ]

        return Response({
            'total_instances': instances.count(),
            'by_status': {
                'in_progress': by_status.get('in_progress', 0),
                'completed': by_status.get('completed', 0),
                'overdue': by_status.get('overdue', 0),
            },
            'average_progress': instances.aggregate(avg=Avg('progress_percent'))['avg'] or 0.0,
            'programs': program_stats,
            'employees_in_onboarding': instances.filter(
                status=OnboardingInstance.Status.IN_PROGRESS
            ).values('employee_id').distinct().count(),
        })
