import hashlib
import json
import time


class User:
    def __init__(self, name, dob, gender, contact_details):
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact_details = contact_details
        self.ehrs = []

    def view_records(self, patient_id):
        """Get all electronic health records (EHRs) of the user."""
        return self.ehrs

    def add_record(self, medical_history, allergies, immunizations, covid_vaccine, lab_results, prescriptions, patient_data):
        """Create a new electronic health record (EHR) for the user."""
        timestamp = time.time()
        ehr = {
            'timestamp': timestamp,
            'medical_history': medical_history,
            'allergies': allergies,
            'immunizations': immunizations,
            'covid-vaccine': covid_vaccine,
            'lab_results': lab_results,
            'prescriptions': prescriptions,
            'patient_data': patient_data
        }
        ehr_hash = hashlib.sha256(json.dumps(
            ehr, sort_keys=True).encode()).hexdigest()
        ehr['hash'] = ehr_hash
        self.ehrs.append(ehr)
        return ehr_hash

    def update_record(self, patient_id, record_id, updated_record):
        """Update an existing EHR record of a specific patient."""
        # Implementation logic for updating EHR records in the blockchain
        pass

    def delete_record(self, patient_id, record_id):
        """Delete an existing EHR record of a specific patient."""
        # Implementation logic for deleting EHR records from the blockchain
        pass

    # Additional methods and functionalities specific to the user type can be added here


user1 = User("XYZ", "25022001", "M", "8726374821")

# name ,date,
