from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    medical_conditions = models.TextField()
    medication_regimen = models.TextField()
    last_appointment = models.DateTimeField()
    next_appointment = models.DateTimeField()
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'patient'
