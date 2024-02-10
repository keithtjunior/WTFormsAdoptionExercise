"""Models for Adopt"""

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, TextAreaField, validators

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Pet"""
    __tablename__ = "pets"

    def get_default_photo_url(self):
        """Return default photo url"""
        return 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'
    
    default_photo_url = property(fget=get_default_photo_url)

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name      = db.Column(db.String(70), nullable=False)
    species   = db.Column(db.String(70), nullable=False)
    age       = db.Column(db.Integer)
    notes     = db.Column(db.String(2200))
    photo_url = db.Column(
                db.String(2048), 
                nullable=False,
                default=get_default_photo_url
            )
    available = db.Column(db.Boolean(), nullable=False, default=True)
    
    def __repr__(self):
        p = self
        return f'<Pet id={p.id} name={p.name} species={p.species} age={p.age} notes={p.notes} photo_url={p.photo_url}>'
    
    def create_pet_from_form(data):
        """Add pet to db using form data"""
        name = data['name'].strip()
        species = data['species'].strip().lower()
        age = data['age']
        notes = data['notes'].strip()
        photo_url = data['photo_url'].strip()
        age = age if age >= 0 else None
        notes = notes if notes else None
        photo_url = photo_url if photo_url else None
        return Pet(name=name, species=species, age=age, notes=notes, photo_url=photo_url)
    
    def edit_pet_from_form(pet, data):
        """Update pet info in db using form data"""
        photo_url = data['photo_url'].strip()
        notes = data['notes'].strip()
        pet.available = data['available']
        pet.notes = notes if notes else None
        pet.photo_url = photo_url if photo_url else pet.default_photo_url

    def remove_form_validators(vals):
        """Temporarily removes validators from flaskform field"""
        for val in vals:
            vals.remove(val)


class AdoptionForm(FlaskForm):
    """Pet wtform data and validation"""
    name         = StringField("Pet's Name", [validators.Length(min=1, max=70), validators.DataRequired()])
    species      = StringField('Species', [
        validators.Length(min=3, max=70), 
        validators.AnyOf(['cat', 'dog', 'porcupine'], message='Species must be either "cat", "dog", or "porcupine"'),
        validators.DataRequired()
    ])
    age          = DecimalField('Age in Years (Optional)', [validators.NumberRange(min=0, max=30), validators.Optional()])
    notes        = TextAreaField('Additional Notes (Optional)', [validators.Length(max=2200), validators.Optional()])
    available    = BooleanField('Pet Available', default='checked')
    photo_url    = StringField('Photo URL (Optional)', [ 
        validators.Length(max=2048), 
        validators.URL(message='Please enter a valid URL'),
        validators.Optional()
    ])
