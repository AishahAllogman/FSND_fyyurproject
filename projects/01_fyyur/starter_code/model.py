from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_description= db.Column(db.String(500), default='')
    seeking_talent = db.Column(db.Boolean, default=False)
    website = db.Column(db.String(120))
    show = db.relationship('Show', backref='Venue', lazy=True)
    #Show = db.relationship("Show", back_populates="Venue")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column("genres",db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), default=' ')
    website = db.Column(db.String(120))
    show = db.relationship('Show', backref='Artist', lazy=True)
    #Show = db.relationship("Show", back_populates="Artist")

    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
       __tablename__ = 'Show'
       show_id = db.Column(db.Integer, primary_key=True)
       Venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=True)
       Artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=True)
       start_time = db.Column(db.DateTime())
      #Venue_id= db.Column(db.Integer,db.ForeignKey('Venue.id'), primary_key=True)
      #Artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'), primary_key=True)
     #start_time = db.Column(String(50))
     #Venue = db.relationship("Artist", back_populates=" Venue")
     #Artist = db.relationship("Venue", back_populates="Artist")
    #db.create_all()
#----------------------------------------------------------------------------#
