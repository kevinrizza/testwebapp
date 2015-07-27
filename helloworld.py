textarea="""
<b>Enter ROT13 text into the text area:</b>
<br>
<br>
<form method="post">
    <textarea type="text" style="height: 100px; width: 400px;" name="text">%(cipher)s</textarea>
    <Input Type="submit">
</form>
"""

form="""
<form method="post">
    <b>Signup</b>
    <br>
    <br>
    <label>Username
	<input type="text" name="username" value=%(username)s>
    </label>
    <div style="color: red">%(usererror)s</div>
    <label>Password
	<input type="text" name="password">
    </label>
    <div style="color: red">%(pworderror)s</div>
    <label>Verify Password
	<input type="text" name="verify">
    </label>
    <div style="color: red">%(pwordmismatch)s</div>
    <label>Email (optional)
	<input type="text" name="email" value=%(email)s>
    </label>
    <div style="color: red">%(emailerror)s</div>
    <br>
    <input type="submit">
</form>
"""

import webapp2
import cgi
import re

class MainPage(webapp2.RequestHandler):
    def write_form(self, usererror="", pworderror="", pwordmismatch="", emailerror="", username="", email=""):
		self.response.out.write(form % {"usererror": usererror,
							"pworderror": pworderror,
							"pwordmismatch": pwordmismatch,
							"emailerror": emailerror,
							"username": cgi.escape(username, quote = True),
							"email": cgi.escape(email, quote = True)})

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        usererror = valid_user(username)
        pworderror = valid_pword(password)
        pwordmismatch = verify_pword(password,verify)
        emailerror = valid_email(email)
        
        if (usererror or pworderror or pwordmismatch or emailerror):
			self.write_form(usererror,pworderror,pwordmismatch,emailerror,username,email)
        else:
			self.redirect("/thanks?username=" + username)
			
class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write("Welcome, " + username + "! Log in successful!")


class Rot13(webapp2.RequestHandler):
    def write_rot(self, cipher=""):
		self.response.out.write(textarea % {"cipher": cgi.escape(cipher)})
	
    def get(self):
        self.write_rot()
    
    def post(self):
        text = self.request.get('text')
        cipher = caesar_cipher(text)
        self.write_rot(cipher)

app = webapp2.WSGIApplication([
    ('/', MainPage),('/thanks',ThanksHandler),('/Rot13',Rot13),
], debug=True)

#Helper Functions

def valid_user(username):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	
	if USER_RE.match(username):
	    return ''
	else:
		return "Invalid username."

def valid_pword(password):
	PWORD_RE = re.compile(r"^.{3,20}$")
	
	if PWORD_RE.match(password):
	    return ''
	else:
		return "Invalid password."
	
def verify_pword(password,verify):
	if(password == verify):
		return ''
	else:
		return "Your passwords didn't match."
	
def valid_email(email):
	EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
	
	if EMAIL_RE.match(email):
	    return ''
	else:
		return "Invalid email."

def caesar_cipher(s):
	cipher=""
	
	if s:
		for ch in s:
			shift = 0
			alpha = ord(ch)
			if(alpha >= ord('A') and alpha <= ord('z')):
				shift = 13
			if( (alpha >= ord('N') and alpha <= ord('Z'))
			 or (alpha >= ord('n') and alpha <= ord('z'))):
				shift*=-1
			char = chr(alpha + shift)
			cipher+= char
	
	return cipher
			
