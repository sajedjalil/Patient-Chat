class Tools:
    def request_medication_change(previous_medication: str) -> str:
        """Puts a request to the doctor for medication change when the previous medication name is mentioned

        Returns a string with the name of current medication and Change request submitted.

        Args:
            previous_medication: first str
        """
        return "Change request submitted for " + previous_medication

    def make_appointment(date: str, reason: str) -> str:
        """Puts an appointment request on the specified date and reason.

        Returns a string with the reason for the requested appointment and date for the appointment

        Args:
            date: first str
            reason: second str
        """
        return "Appointment requested on " + date + " for " + reason

    def request_appointment_change(past_date: str, requested_date: str) -> str:
        """Puts an appointment change request for a given date and requested.

        Returns a string with the changed and previous date for appointment.

        Args:
            past_date: first str
            requested_date: second str
        """
        return past_date + " " + requested_date
