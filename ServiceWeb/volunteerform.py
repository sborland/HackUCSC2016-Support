import web
from flask import request, redirect

urls = (
  '/', 'signup'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/')

if __name__ == "__main__":
    app.run()