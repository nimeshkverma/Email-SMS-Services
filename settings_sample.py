
# Please provide the API key for the account made on the website 2factor.in
SMS_GATEWAY_API_KEY = 'SMS_GATEWAY_API_KEY'

# Provide the 2factor urls for each type of sms
SMS_GATEWAY_URL = {
    'otp': 'http://2factor.in/API/V1/{api_key}/SMS/',
    'transactional': 'http://2factor.in/API/V1/{api_key}/ADDON_SERVICES/SEND/TSMS',
    'promotional': 'http://2factor.in/API/V1/{api_key}/ADDON_SERVICES/SEND/PSMS'
}
