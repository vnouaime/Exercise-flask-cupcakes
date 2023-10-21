from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddCupcakeForm(FlaskForm): 
    """ Form for creating new cupcake """

    flavor = StringField("Flavor", 
                         validators=[InputRequired()])
    size = StringField("Size", 
                         validators=[InputRequired()])
    rating = FloatField("Rating", 
                         validators=[InputRequired()])
    image = StringField("Image URL",
                           validators=[
                            Optional(), 
                            URL(message="Invalid URL. Please enter a valid URL")])

