# MapApp/management/commands/update_activation_state.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from MapApp.models import Operation
import pytz

class Command(BaseCommand):
    help = 'Update activation state of UTM operations based on current time'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        operations = Operation.objects.filter(request_state='approved')
        changes_made = False
        for operation in operations:
            previous_state = operation.activation_state
            if now < operation.start_datetime:
                operation.activation_state = 'inactive'
            elif operation.start_datetime <= now <= operation.end_datetime:
                operation.activation_state = 'active'
            else:
                operation.activation_state = 'expired'
            if operation.activation_state != previous_state:
                changes_made = True
            operation.save()
        if changes_made:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated activation states at {now.astimezone(pytz.utc)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'No changes made to activation states at {now.astimezone(pytz.utc)}'))