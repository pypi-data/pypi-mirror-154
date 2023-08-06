import pyotp

def generator():
	return pyotp.random_base32()

class secret:
	def __init__(self, secretkey):
		self.secretkey = secretkey

	def code(self):
		secretkey = self.secretkey
		sec2 = pyotp.TOTP(secretkey)
		return sec2.now()

	def verify(self, code):
		secretkey = self.secretkey
		sec2 = pyotp.TOTP(secretkey)
		return sec2.verify(code) 
