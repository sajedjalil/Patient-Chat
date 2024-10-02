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
        return (f"Patient Name: {self.first_name} {self.last_name}, "
                f"Date of Birth: {self.date_of_birth}, "
                f"Phone: {self.phone_number}, "
                f"Email: {self.email}, "
                f"Medical Conditions: {self.medical_conditions}, "
                f"Medication: {self.medication_regimen}, "
                f"Last Appointment: {self.last_appointment}, "
                f"Next Appointment: {self.next_appointment}, "
                f"Current Doctor Name: {self.doctor_name}\n")


    class Meta:
        db_table = 'patient'
