from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key yo"

class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# filters #

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags 




@app.route('/')
def index():
    first_name = "Julian"
    stuff = "This is Bold Text"

    favorite_pizza= ["Pepperoni", "Cheese", "Onions", 41]
    return render_template('index.html', 
        first_name=first_name,
        stuff=stuff,
        favorite_pizza=favorite_pizza) 

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data= ''

    return render_template('name.html', 
        name=name, 
        form=form)











if __name__ == "__main__":
    app.run(debug=True)