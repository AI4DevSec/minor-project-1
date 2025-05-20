# src/custom_exception.py

import sys # System ki jankari lene ke liye

# Hamara apna special tarah ka error reporter banate hain
class CustomException(Exception): # Yeh normal Exception wali family se hai
    def __init__(self, message: str, error_detail: Exception = None):
        # Jab yeh reporter banega, isko ek message aur original galti (error_detail) do
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message) # Parent Exception class ko hamara detailed message de do

    @staticmethod # Yeh function seedha class se use ho sakta hai, robot banane ki zarurat nahi
    def get_detailed_error_message(message, error_detail):
        """Error message ko detail mein format karta hai (kahaan galti hui)."""
        _, _, exc_tb = sys.exc_info() # Galti ke time ki details nikalo
        # Pata lagao ki kaunsi file aur kaunsi line mein galti hui
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown File"
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown Line"
        # Ek achha detailed message banao
        return f"{message} | Error: {error_detail} | File: {file_name} | Line: {line_number}"

    def __str__(self):
        """Jab is reporter ko print karenge, toh yeh message dikhega."""
        return self.error_message