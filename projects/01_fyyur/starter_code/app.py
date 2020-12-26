#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from collections import Counter
from model import *
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#

# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format,locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#---------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')

 
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
 
def venues():
  data=[]
  venues=Venue.query.group_by(Venue.city,Venue.state,Venue.id) 

  nowtime=datetime.now()
  for venue in venues: 
    Numshow=Show.query.join(Venue).filter(Show.Venue_id==venue.id).filter(nowtime<Show.start_time).all()
    num_upcomingshow=len(Numshow)
    data.append({
      "city":venue.city,
      "state":venue.state,
      "venues":Venue.query.filter(Venue.city==venue.city).filter(Venue.state==venue.state).all(),
      "num_up_coming_show":Numshow
    })
      
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_criteria=request.form.get('search_term', '')
  search=Venue.query.filter(Venue.name.ilike('%'+search_criteria+'%')).all()
  modelcount= len(search)
  mydata = []
  for numsearch in search: 
     # Shows = Show.query.join(Venue,Artist).filter_by(numsearch.id==id)
      #for S in Shows:
      #if (Shows.starttime>localtime):
      # num_upcoming_shows=num_upcoming_shows+1
      mydata.append({
      "id":numsearch.id,
      "name":numsearch.name,
      "num_upcoming_shows": 0,#num_upcoming_shows
    })
  
  response={
    "count":len(search),
    "data":mydata
    }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venueid=int(venue_id)
  #data =[]
  #artist=Artist.query.filter((Artist.id==artistid).all()
  venuesearch = Venue.query.get(venueid)
  
  data1=[]
  past_shows=[]
  upcomingshows=[]
  nowtime=datetime.now()
  upcoming_shows=0
  past_show_show=0

  Shows = Show.query.join(Venue).filter(Show.Venue_id==venueid).all()
 #i try to do it 2 fillter  depanded (id and when start)
  for Venueview in Shows:
    if nowtime > Venueview.start_time:
      upcomingshow = Show.query.join(Venue).filter(Show.Venue_id==venueid).filter(nowtime>Venueview.start_time).all()
      for cs in upcomingshow :
        upcomingshows.append({
        "artist_id":cs.Artist_id,
        "artist_name":cs.Artist.name ,
        "artist_image_link":cs.Artist.image_link ,
        "start_time":str(cs.start_time)
        }) 
      upcoming_shows=upcoming_shows+1 
    if nowtime < Venueview.start_time:
      pastshow = Show.query.join(Venue).filter(Show.Venue_id==venueid).filter(nowtime<Venueview.start_time).all()
      for ps in pastshow :
        past_shows.append({
          "artist_id":ps.Artist_id,
          "artist_name":ps.Artist.name ,
          "artist_image_link":ps.Artist.image_link ,
          "start_time":str(ps.start_time)
          }) 
        past_show_show=past_show_show+1 
      
    data1={
      "id": Venueview.Venue.id,
      "name": Venueview.Venue.name,
      "city": Venueview.Venue.city,
      "state": Venueview.Venue.state,
      "phone":Venueview.Venue.phone,
      "facebook_link": Venueview.Venue.facebook_link,
      "image_link": Venueview.Venue.image_link,
      "seeking_talent": True,
      "past_shows": past_shows,
      "upcoming_shows":upcomingshows,
      "past_shows_count":past_show_show,
      "upcoming_shows_count":upcoming_shows
      }


  data =data1
    

  #data = list(filter(lambda d: d['id'] == Venuesearch, [data1]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['Post'])
def create_venue_submission():
    form = VenueForm()
    error=False
    try:
      newvenue = Venue(
      name=request.form['name'],
      address=request.form['address'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link']
    )
      db.session.add(newvenue)
      db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
      db.session.close()
    if error:
      print ("error")
      flash('Venue' + request.form['name'] + ' unsuccessfully listed!')
    else:
      flash('Venue' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')
        
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  id=int(venue_id)
  error = False 
  try :
    venuee = Venues.query.get(id) 
    db.session.delete(venuee)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
      db.session.close()
  if error :
      print ("error")
      flash('delete venuee ' + venue_id + ' unsuccessfully ')
  else:
      flash('delete venuee ' + venue_id   + ' was successfully !')
      return render_template('pages/home.html')

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
 data = db.session.query(Artist).all()
 return render_template('pages/artists.html', artists=data)
  

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_criteria=request.form.get('search_term', '')
  search=Artist.query.filter(Artist.name.ilike('%'+search_criteria+'%')).all()
  modelcount= len(search)
  mydata=[]
  for numsearch in search: 
    mydata.append({
      "id":numsearch.id,
      "name":numsearch.name,
      "num_upcoming_shows": 0,
    })
  
  response={
    "count":len(search),
    "data":mydata
    }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artistid=int(artist_id)
  #data =[]
  #artist=Artist.query.filter((Artist.id==artistid).all()
  Artistsearch = Artist.query.get(artistid)
  
  data=[]
  past_shows=[]
  upcomingshows=[]
  nowtime=datetime.now()
  upcoming_shows=0
  past_show_show=0
  Shows = Show.query.join(Artist).filter(Show.Artist_id==artistid).all()
 #i try to do it 2 fillter  depanded (id and when start)
  for artistview in Shows:
    if nowtime > artistview.start_time:
      upcomingshow = Show.query.join(Artist).filter(Show.Artist_id==artistid).filter(nowtime>artistview.start_time).all()
      for cs in upcomingshow :
        upcomingshows.append({
          "venue_id":cs.Venue_id,
          "venue_name":cs.Venue.name ,
          "venue_image_link":cs.Venue.image_link ,
          "start_time":str(cs.start_time)
         }) 
        upcoming_shows=upcoming_shows+1 
    if nowtime < artistview.start_time:
      pastshow = Show.query.join(Artist).filter(Show.Artist_id==artistid).filter(nowtime<artistview.start_time).all()
      for ps in pastshow :
        past_shows.append({
          "venue_id":ps.Venue_id,
          "venue_name":ps.Venue.name ,
          "venue_image_link":ps.Venue.image_link ,
          "start_time":str(ps.start_time)
         }) 
        past_show_show=past_show_show+1 
    
    data1={
      "id": artistview.Artist.id,
      "name": artistview.Artist.name,
      "genres":artistview.Artist.genres,
      "city": artistview.Artist.city,
      "state": artistview.Artist.state,
      "phone":artistview.Artist.phone,
      "facebook_link": artistview.Artist.facebook_link,
      "image_link": artistview.Artist.image_link,
      "seeking_talent": True,
      "past_shows": past_shows,
      "upcoming_shows":upcomingshows,
      "past_shows_count":past_show_show,
      "upcoming_shows_count":upcoming_shows
    }
  data =data1
   
  #data = list(filter(lambda d: d['id'] == artist_id,[data1]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  id=int(artist_id)
  artistedit= Artist.query.get(id)
  data=[]
  data.append({
      "id":artistedit.id,
      "name":artistedit.name,
      "genres":artistedit.genres,
      "city":artistedit.city,
      "state":artistedit.state,
      "phone":artistedit.phone,
      "facebook_link":artistedit.facebook_link
      })
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artistedit )

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  id=int(artist_id)
  sid = Artist.query.get(id)
  updateArtist=[]
  sid.name=request.form['name'],
  sid.genres=request.form.getlist('genres'),
  sid.address=request.form['address'],
  sid.city=request.form['city'],
  sid.state=request.form['state'],
  sid.phone=request.form['phone'],
  sid.facebook_link=request.form['facebook_link'],
   

  db.session.add(sid)
  db.session.commit()
  
      
    
  Artist.Update(updatArtist)
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  id=int(venue_id)
  venueid =Venue.query.get(id)
  data=[]
  data.append({
    "id":venueid.id,
    "name":venueid.name,
    "city": sid.city,
    "state": sid.state,
    "phone": sid.phone,
    "facebook_link": sid.facebook_link,
  })
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venueid)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  updateVenue=[]
  updatVenue = Venue(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      address=request.form['address'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link'],
      image_link=request.form['image_link']
    )
  Venue.Update(updatVenue)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form =ArtistForm()

  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  error=False
  try:
    newartist = Artist(
      name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link']
    )
    db.session.add(newartist)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()

  if error : 
      flash('Artist ' + request.form['name'] + ' was unsuccessfully listed!')
  else :
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success

  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  Shows = Show.query.join(Venue,Artist).all()
  data=[]
  for s in Shows:
    data.append({ 
    "venue_id":s.Venue_id,
    "venue_name":s.Venue.name,
    "artist_id":s.Artist_id,
    "artist_name":s.Artist.name,
    "artist_iamge_link":s.Artist.image_link,
    "start_time":str(s.start_time)
    })
 
  return render_template('pages/shows.html', shows=data)
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.





@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  error=False
  try:
    newshow = Show(
    Venue_id=request.form['Venue_id'],
    Artist_id=request.form['Artist_id'],
    start_time=request.form.form['start_time']
    )
    db.session.add(newshow)
    db.session.commit()

  except():
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error :
      flash('Show unsuccessfully listed!')
    else:
      flash('Show was successfully listed!')
      return render_template('pages/home.html')
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
 # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
