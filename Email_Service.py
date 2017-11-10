import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import exc_info

SMTP_SERVER = "smtp_server"
SMTP_SERVER_PORT ="smtp_server_port"
GMAIL_USER = "user"
GMAIL_PWD = "password"
SENDER = "From"
RECEIVERS = "To"
SUBJECT = "Subject"
CONTENT = "Body"
ERROR = "error"
CONNECTION = "connection"

class EmailService(object) :
	""" Class to enable sending of emails """

	def __init__(self, settings_file) :
		""" Accepts the name of the file that holds the server details, etc """
		if settings_file:
			self.settings_file = settings_file
		else :
			self.settings_file = "None"

	def __populate_settings(self) :
		# Utility method to extract the mail server details and others from the settings file
		# This method is not to be overridden by the subclasses

		server_dict = {}
		if self.settings_file != "None" :
			try :
				file_obj = open(self.settings_file, "r")
				str = file_obj.read()
			except:
				# could not open the file
				server_dict[ERROR] = "Settings file is not available"
				return server_dict

			if (str and str != "") : 
				# file is not empty and key=value pairs expected on separate lines 
				list_str = str.split("\n")
				for elem in list_str:
					list_elem = elem.split("=")
					if (list_elem and list_elem[0] == RECEIVERS and len(list_elem) == 2) :
						# in the case of RECEIVERS, the value is a list, so take off the list brackets
						list_str = list_elem[1][1:-1] 
						server_dict[list_elem[0]] = list_str
					elif (list_elem and len(list_elem) == 2):
						server_dict[list_elem[0]] = list_elem[1]
					else :
						# Settings file does not have information as key=value pairs
						server_dict[ERROR] = "Settings file does not have information as key=value pairs"       
			else :
				# Settings file could be empty
				server_dict[ERROR] = "Insufficient information in Settings file"
		else :
			# Settings file not present
			server_dict[ERROR] = "Settings file is not available"

		return server_dict

	
	def __connect_to_server(self) :
		# Utility method to establish a connection with the mail server
		# This method is not to be overridden by the subclasses
		
		server_dict = self.__populate_settings()
		if (server_dict and ERROR not in (server_dict.keys())):
			server_str = server_dict[SMTP_SERVER]
			server_port = int(server_dict[SMTP_SERVER_PORT])

			if (server_str != None and server_port > 0) :
				try :
						# creating a secure SSL connection to the email server 
						server_ssl = smtplib.SMTP_SSL(server_str, server_port)
						server_ssl.ehlo()   # optional
						server_dict[CONNECTION] = server_ssl
				except:
						server_dict.clear()
						server_dict[ERROR] = "Unable to connect to server %s " %server_str   
			else :
				server_dict.clear()
				server_dict[ERROR] = "Incorrect Server details %s, %d" %(server_str, server_port)
		
		return server_dict

	def __compose_html_content(self, subject, send_from, send_to, body):
		# Composes the email content in the HTML format

		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg[SUBJECT] = subject
		msg[SENDER] = send_from
		msg[RECEIVERS] = send_to
		list_content = body.split("\\n") # to handle multiline body

		# Create the body in HTML format.
		html = """ <html>
					<head></head>
					<body>
					<p> <b> """
		for elem in list_content:
			html += elem + "<br>" 
			
		html += """ <b> </p>
					</body>
					</html> """

		# Record the MIME type text/html.
		html_body = MIMEText(html, 'html')

		# Attach parts into message container.
		msg.attach(html_body)
		return msg.as_string()


	def send_email_SMTP(self) :
		""" Public method used to send email """

		server_dict = self.__connect_to_server()
		if (server_dict and CONNECTION in server_dict.keys()) :
			# extract info from server_dict
			server_conn = server_dict[CONNECTION]
			try :
				user = server_dict[GMAIL_USER]
				pwd = server_dict[GMAIL_PWD]
	
				send_from = server_dict[SENDER] 
				send_to = server_dict[RECEIVERS] 
				if (type(send_to) is list) : # implies multiple recipients
					send_to = ", ".join(send_to)
				subject = server_dict[SUBJECT]
				body = server_dict[CONTENT]
			except KeyError:
				print " Insufficient key=value pairs in Settings file "
				return # equivalent to returning None

			content_str = self.__compose_html_content(subject, send_from, send_to, body)
			# first we could verify if the email id and password are valid
			is_valid = self.__validate_email(user)
			if is_valid :
				try :
					server_conn.login(user, pwd)
					server_conn.sendmail(send_from, send_to, content_str)
					server_conn.close()
					print " Email sent successfully! "
				except:
					print " Sending mail from %s to %s failed " %(send_from, send_to)
					e = exc_info()[0]
					print " Error: %s " %e
				finally:
					if server_conn:
						server_conn.close()
			else :
				print " Invalid Sender's email id %s " %user
		else :
			if server_dict and ERROR in server_dict.keys():
				print server_dict[ERROR]
	

	def send_email(self, send_from, send_to, subject = "", message_body = "") :
		""" Public method used to send email mentioning other details """

		if (send_from == None or send_to == None) :
			print " Incorrect arguments to send email "
			return

		server_dict = self.__connect_to_server()
		if (server_dict and CONNECTION in server_dict.keys()) :
			# extract info from server_dict
			server_conn = server_dict[CONNECTION]
			try :
				user = server_dict[GMAIL_USER]
				pwd = server_dict[GMAIL_PWD]
	
			except KeyError:
				print " Insufficient key=value pairs in Settings file "
				return 

			# Commenting out this check for now
			if (self.__isvalid_sender_recipient(send_from, send_to) == False) :
				# sender or recipient or both email IDs are invalid
				return

			content_str = self.__compose_html_content(subject, send_from, send_to, message_body)
			# first we could verify if the email id and password are valid
			is_valid = self.__validate_email(user)
			if is_valid :
				try :
					server_conn.login(user, pwd)
					server_conn.sendmail(send_from, send_to, content_str)
					server_conn.close()
					print " Email sent successfully! "
				except:
					print " Sending mail from %s to %s failed " %(send_from, send_to)
					e = exc_info()[0]
					print " Error: %s " %e
				finally:
					if server_conn:
						server_conn.close()
			else :
				print " Invalid Sender email id %s " %user
		else :
			if server_dict and ERROR in server_dict.keys():
				print server_dict[ERROR]


	def __validate_email(self, email_id) :
		# Utility method to validate email IDs
		return re.match("([^@|\s]+@[^@]+\.[^@|\s]+)", email_id)

		
	def __isvalid_sender_recipient(self, send_from, send_to) :
		# Utility method to check if sender and recipient email IDs are valid 
		if self.__validate_email(send_from) :
			# sender address is valid
			if send_to.index(",") > 0:
				# multiple recipients
				list_str = send_to.split(",")
				for elem in list_str:
					if(self.__validate_email(elem) == False) :
						print " Invalid recipient email address = %s " %(elem)               
						return False
			else :
				if(self.__validate_email(send_to) == False) :
					print " Invalid recipient email address = %s " %(elem)
					return False
			# Control reached here => both valid
			return True
		else :
			print " Invalid sender email address = %s " %(send_from)
			return False




