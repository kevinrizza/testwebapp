import os
import webapp2
import cgi
import re
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def write_form(self, usererror="", pworderror="", pwordmismatch="", emailerror="", username="", email=""):
		self.render("login.html",usererror=usererror,
								 pworderror=pworderror,
								 pwordmismatch=pwordmismatch,
								 emailerror=emailerror,
								 username=username,
								 email=email)

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
			
class Thanks(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write("Welcome, " + username + "! Log in successful!")


class Rot13(Handler):
    def write_rot(self, cipher=""):
		self.render('rot13.html', cipher=cipher)
	
    def get(self):
        self.write_rot()
    
    def post(self):
        text = self.request.get('text')
        cipher = caesar_cipher(text)
        self.write_rot(cipher)
        
class ShoppingPage(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list.html", items=items)
		
class FizzBuzz(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render('fizzbuzz.html', n = n)

app = webapp2.WSGIApplication([
    ('/', MainPage),('/thanks',Thanks),('/rot13',Rot13),('/fizzbuzz',FizzBuzz),('/shopping',ShoppingPage),
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
	
	if (EMAIL_RE.match(email) or email == ''):
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
			
