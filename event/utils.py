



class Notification:
    def __init__(self, location: str, name: str, message: str, contact: dict[ str, str]):
        self.location = location
        self.name = name
        self.message = message
        self.contact = contact

    def send_notification(self):
        pass

    def send_sms(self):
        pass

    def send_email(self):
        pass

    def send_whatsapp(self):
        pass
