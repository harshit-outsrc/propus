class UserIdTaken(Exception):
    def __init__(self, sis_id, user_type, message=None):
        self.sis_id = sis_id
        self.message = message if message else f"SIS ID '{sis_id}' for user type '{user_type}' is already in use."
        super().__init__(self.message)
