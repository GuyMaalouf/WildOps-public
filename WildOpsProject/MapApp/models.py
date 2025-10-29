from django.db import models
from shared.constants import OPERATION_TYPE_CHOICES, DRONE_PLATFORM_CHOICES, NUMBER_OF_DRONES_CHOICES, UAS_CHOICES, PILOT_CHOICES

class Operation(models.Model):
    REQUESTED = 'requested'
    APPROVED = 'approved'
    DECLINED = 'declined'
    REQUEST_STATUS_CHOICES = [
        (REQUESTED, 'Requested'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    ]

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    EXPIRED = 'expired'
    ACTIVATION_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (EXPIRED, 'Expired'),
    ]

    operation_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)  # Username of the person filling the form
    rpic = models.CharField(max_length=100, choices=PILOT_CHOICES)  # RPIC: Remote Pilot in Command
    uas = models.CharField(max_length=100, choices=UAS_CHOICES)  # UAS platform with individual ID
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.DecimalField(max_digits=5, decimal_places=2)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    request_state = models.CharField(
        max_length=10,
        choices=REQUEST_STATUS_CHOICES,
        default=REQUESTED,
    )
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPE_CHOICES, default='VLOS')
    drone_platform = models.CharField(max_length=20, choices=DRONE_PLATFORM_CHOICES, default='DJI')
    number_of_drones = models.CharField(max_length=20, choices=NUMBER_OF_DRONES_CHOICES, default='SINGLE')
    activation_state = models.CharField(
        max_length=12,
        choices=ACTIVATION_STATUS_CHOICES,
        default=INACTIVE,
    )

    def __str__(self):
        return f"{self.operation_id} - {self.operation_type} - {self.drone_platform}"
    
    class Meta:
        permissions = [
            ("view_olpejeta", "Can view Ol Pejeta"),
            ("view_flightcylinders", "Can view flight cylinders"),
            ("view_utm", "Can view UTM"),
            ("view_operationrequest", "Can view operation request"),
        ]