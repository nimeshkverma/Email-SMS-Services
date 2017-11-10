from Email_Service import EmailService 

if __name__ == "__main__":
	# Creating an instance of the EmailService class
	email_service = EmailService("settings_email.txt")
	# Sending out an email using the service
	email_service.send_email_SMTP()

	email_send = EmailService("settings_email.txt")
	# Sending out email passing arguments 
	email_send.send_email("ddharmarajan@gmail.com", "ddharmarajan@yahoo.com, a@b.com", "Test", "Hello!!!")
