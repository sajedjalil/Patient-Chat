class Tools:
    def request_medication_change( current_medication: str) -> str:
        """Puts a request to the doctor for medication change when the current medication name is mentioned

        Returns a string with the name of current medication and Change request submitted.

        Args:
            current_medication: first str
        """
        return "You have made a medication change request for: " + current_medication

    def request_appointment_change( requested_date: str) -> str:
        """Puts an appointment change request for a requested given date.

        Returns a string with the requested date for appointment.

        Args:
            requested_date: first str
        """
        return "You have made an appointment Request on: " + requested_date
