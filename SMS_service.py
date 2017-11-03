import copy
import requests
import settings


class TwoFactorSMS(object):
    """Class for SMS and its utilities using the thirtparty client: 2factor.in"""

    def __init__(self, receiver, sender=None):
        self.receiver = receiver
        self.sender = sender

    def __get_sms_gateway_url(self, sms_type):
        if sms_type == "promotional":
            return settings.SMS_GATEWAY_URL['promotional'].format(api_key=settings.SMS_GATEWAY_API_KEY)
        elif sms_type == "transactional":
            return settings.SMS_GATEWAY_URL['transactional'].format(api_key=settings.SMS_GATEWAY_API_KEY)
        elif sms_type == "otp":
            return settings.SMS_GATEWAY_URL['otp'].format(api_key=settings.SMS_GATEWAY_API_KEY)
        else:
            return None

    def promotional(self, message, send_at=None):
        payload = {
            'From': self.sender,
            'To': self.receiver,
            'Msg': message,
        }
        if send_at:
            payload['SendAt'] = send_at
        url = self.__get_sms_gateway_url('promotional')
        response = requests.request("POST", url, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False

    def transactional(self, template, var_data):
        payload = copy.deepcopy(var_data)
        payload.update({
            'From': self.sender,
            'To': self.receiver,
            'TemplateName': template,
        })
        url = self.__get_sms_gateway_url('transactional')
        response = requests.request("POST", url, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False

    def otp(self, otp_code, template):
        otp_url_part = '{mobile_number}/{otp_code}/{template}'.format(mobile_number=self.receiver,
                                                                      otp_code=otp_code,
                                                                      template=template)
        url = self.__get_sms_gateway_url('otp') + otp_url_part
        response = requests.request("GET", url)
        if response.status_code == 200:
            return True
        else:
            return False
