#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/events')
def get_events():
    """GET /events: Returns a list of all events with id, name, and location"""
    events = Event.query.all()
    events_data = []
    
    for event in events:
        events_data.append({
            "id": event.id,
            "name": event.name,
            "location": event.location
        })
    
    return jsonify(events_data), 200

@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    """GET /events/<int:id>/sessions: Returns all sessions for a given event"""
    event = Event.query.filter_by(id=id).first()
    
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    sessions_data = []
    for session in event.sessions:
        sessions_data.append({
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        })
    
    return jsonify(sessions_data), 200

@app.route('/speakers')
def get_speakers():
    """GET /speakers: Returns a list of all speakers with id and name"""
    speakers = Speaker.query.all()
    speakers_data = []
    
    for speaker in speakers:
        speakers_data.append({
            "id": speaker.id,
            "name": speaker.name
        })
    
    return jsonify(speakers_data), 200

@app.route('/speakers/<int:id>')
def get_speaker(id):
    """GET /speakers/<int:id>: Return a speaker with their bio"""
    speaker = Speaker.query.filter_by(id=id).first()
    
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    
    # Check if speaker has a bio
    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    
    speaker_data = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }
    
    return jsonify(speaker_data), 200

@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    """GET /sessions/<int:id>/speakers: Returns a list of speakers for a session"""
    session = Session.query.filter_by(id=id).first()
    
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    speakers_data = []
    for speaker in session.speakers:
        bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
        speakers_data.append({
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": bio_text
        })
    
    return jsonify(speakers_data), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)