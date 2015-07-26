textarea="""
<b>Enter ROT13 text into the text area:</b>
<br>
<br>
<form method="post" action="/Rot13">
    <textarea name="text"></textarea>
    <Input Type="submit">
    <Input Type="reset">
</form>
"""

import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
	

class Rot13(webapp2.RequestHandler):
    def get(self):
        self.response.write(textarea)
    def post(self):
	self.response.write(textarea)

app = webapp2.WSGIApplication([
    ('/', MainPage),('/Rot13',Rot13),
], debug=True)
