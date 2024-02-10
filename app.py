"""Adopt application."""

from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet, AdoptionForm

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'aloneintheworldwasalittlecatdog413'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    # app.logger.info('variable: %s', variable)
    # import pdb;  pdb.set_trace()
    # records = [dict(zip(pet.keys(), pet)) for pet in pets]
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Add a new pet"""
    try:
        form = AdoptionForm()
        if request.method == 'POST' and form.validate_on_submit():
            new_pet = Pet.create_pet_from_form(form.data)
            db.session.add(new_pet)
            db.session.commit()
            flash(f'Pet added.', 'success')
            return redirect('/')
        return render_template('add-pet.html', form=form)
    except:
        flash(f'There was an error adding pet. Please try again.', 'danger')
        return redirect('/')

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_user(pet_id):
    """Show details about a pet with a form to edit pet info"""
    try:
        pet = Pet.query.get_or_404(pet_id)
        form = AdoptionForm()
        form.notes.label = 'Additional Notes'
        form.photo_url.label = 'Photo URL'
        Pet.remove_form_validators(form.name.validators)
        Pet.remove_form_validators(form.species.validators)
        if request.method == 'GET':
            form.notes.data = pet.notes
            form.available.data = pet.available
        if request.method == 'POST' and form.validate_on_submit():
            Pet.edit_pet_from_form(pet, form.data)
            db.session.commit()
            flash(f'Pet updated.', 'success')
            return redirect(f'/{pet_id}')
        return render_template("pet-details.html", pet=pet, form=form)
    except:
        flash(f'There was an error updating pet. Please try again.', 'danger')
        return redirect(f'/{pet_id}')
        
    
