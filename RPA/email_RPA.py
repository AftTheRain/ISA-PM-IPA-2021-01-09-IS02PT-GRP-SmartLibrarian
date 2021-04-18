from useful_lib import wait_for_pageload
import rpa as t


class Email:

	def __init__(self):
		self.url = 'https://mail.google.com/'
		self.sign_in_url = f'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'


	def has_signed_in(self):

		if t.present('//div[@role="button"][.="Compose"]'):
			print(f'Signed in to email account')
			print(f'')
			return True

		else:
			print(f'Not signed in to email account')
			print(f'')
			return False

	def sign_in(self):
		t.url(self.sign_in_url)
		print(f'Going to: {self.sign_in_url}')
		print(f'')
		wait_for_pageload('//div[@class="rr0DNb"]')
		print(f'Waiting for sign in details')
		print(f'')
		wait_for_pageload('//div[@role="button"][.="Compose"]', 120)



	def compose_email(self, body, subject = '', mail_to = ''):

		try:
			t.init()
			t.url(self.url)
			t.wait(5)

			if not self.has_signed_in():
				self.sign_in()

			if mail_to == '':
				t.click('//img[@class="gb_Da gbii"]')
				mail_to = t.read('//div[@class="gb_ob"]')

			t.hover('//div[@role="button"][.="Compose"]')
			t.click('//div[@role="button"][.="Compose"]')

			t.type('//table[@class="GS"]/../following-sibling::div[1]/div[1]', mail_to)
			t.type('//input[@name="subjectbox"]', subject)
			t.type('//div[@role="textbox"]', body)
			t.wait(20)
			t.click('//div[@role="button"][.="Send"]')

		finally:
			t.close()
#main
if __name__ == "__main__":
	email_recipient = ''
	try:
		with open('email_recipient.txt') as f:
			email_recipient = f.readlines()[0][:-1]
	except:
		pass

	email = Email()
	email.compose_email(subject='Automated Email', body='This is a test', mail_to=email_recipient)
