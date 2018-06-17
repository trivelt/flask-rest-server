from IPy import IP


class DataValidator(object):

    @staticmethod
    def is_invalid_ip(address):
        try:
            IP(address)
            return False
        except:
            return True
