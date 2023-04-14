class EHRUser:
    def __init__(self, user_id, user_type):
        self.user_id = user_id  # unique identifier for the user
        # type of user (e.g., patient, physician, hospital)
        self.user_type = user_type

    def view_records(self, patient_id):
        """View EHR records of a specific patient."""
        # Implementation logic for viewing EHR records from the blockchain
        pass

    def add_record(self, patient_id, record):
        """Add a new EHR record for a specific patient."""
        # Implementation logic for adding EHR records to the blockchain
        pass

    def update_record(self, patient_id, record_id, updated_record):
        """Update an existing EHR record of a specific patient."""
        # Implementation logic for updating EHR records in the blockchain
        pass

    def delete_record(self, patient_id, record_id):
        """Delete an existing EHR record of a specific patient."""
        # Implementation logic for deleting EHR records from the blockchain
        pass

    # Additional methods and functionalities specific to the user type can be added here
