class Target:
    def __init__(self, target_name: str = "t1",first_name: str = None, surname: str = None, email_address: str = None):

        self.target_name = target_name

        # Basic contact info
        self.first_name = first_name
        self.surname = surname
        self.email_address = email_address
        self.ip_address = None
        self.phone_number = None

        # OSINT findings
        self.email_breaches: dict = {}
        self.social_media_profiles: dict = {}
        self.whois_info: dict = {}
        self.dns_records: dict = {}
        self.geolocation_info: dict = {}

        self.raw_api_responses: dict = {}
