from SMS_service import TwoFactorSMS

if __name__ == '__main__':
    # Making an object of the TwoFactorSMS class
    two_factor_sms = TwoFactorSMS('9911616971', 'StartupName')

    # Sending OTP
    print two_factor_sms.otp('1234', 'otp_template')

    # Sending Transactional SMS
    var_data = {
        'VAR1': 'Customer Name',
        'VAR2': 'Status of the product'
    }
    print two_factor_sms.transactional('transaction_template', var_data)

    # Sending Promotional SMS
    print two_factor_sms.promotional('Hello User, Please download our App')
