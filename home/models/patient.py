from django.db import models


class Patient(models.Model):
    """
    This class represents a patient in a medical system.

    Attributes:
    first_name (CharField): The patient's first name.
    last_name (CharField): The patient's last name.
    date_of_birth (DateField): The patient's date of birth.
    phone_number (CharField): The patient's phone number.
    email (EmailField): The patient's email address.
    medical_conditions (TextField): The patient's medical conditions.
    medication_regimen (TextField): The patient's medication regimen.
    last_appointment (DateTimeField): The date and time of the patient's last appointment.
    next_appointment (DateTimeField): The date and time of the patient's next appointment.
    doctor_name (CharField): The name of the patient's current doctor.

    Methods:
    __str__(): Returns a string representation of the patient's details.
    """

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

    # Mapping for database table name
    class Meta:
        db_table = 'patient'
