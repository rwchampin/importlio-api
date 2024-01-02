from .models import UserAccount

class Manager:
    def __init__(self):
        self.account = None
    
    @staticmethod
    def get(email):
        # get user account or return none
        try:
            return UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            return None
        