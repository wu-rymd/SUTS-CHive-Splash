from flask import Flask, request, jsonify, render_template, Response, send_from_directory
from lib.db import dbconnect, db_create, School, User, Club, UserToClubMapping, Message
import json
import hashlib
import os

app = Flask(__name__)

db_options = {'db_file': 'my.db'}


# for login authentication
def hashString(string):
    return hashlib.sha256(string).hexdigest()


def get_or_create_school(session, school_name, address):
    school = session.query(School).filter(School.name == school_name).one_or_none()
    if school:
        return school
    school = School(name=school_name, address=address)
    session.add(school)
    session.flush()
    return school.id


@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    Session, engine = dbconnect(db_options)
    session = Session()
    users = session.query(User).filter(User.username == username).all()
    ret_users = []
    for u in users:
        ret_users.append(
            {
                'id': u.id,
                'username': u.username,
                'first': u.first_name,
                'last': u.last_name
            }
        )
    #users = map(lambda u: dict(u), users)
    return jsonify(ret_users)


@app.route('/user', methods=['POST'])
def create_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    user = User(
        first_name=j.get('first_name'),
        last_name=j.get('last_name'),
        username=j.get('username'),
        password=hashString(j.get('password')),
        school_id=get_or_create_school(session, j.get('school')),
        email=j.get('email')
    )
    session.add(user)
    session.flush()
    session.commit()
    return jsonify(
        {
            'id': user.id
        }
    )


@app.route('/user', methods=['PUT'])
def modify_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    userID = j.get('id')
    matchingUser = session.query(User).filter(User.id == userID).one_or_none()
    if matchingUser:
        if j.get('first_name') != None:
            matchingUser.first_name=j.get('first_name')
        if j.get('last_name') != None:
            matchingUser.last_name=j.get('last_name')
        if j.get('username') != None:
            matchingUser.username=j.get('username')
        if j.get('password') != None:
            matchingUser.password=hashString(j.get('password'))
        if j.get('school_id') != None:
            matchingUser.school_id=j.get('school_id')
        if j.get('email') != None:
            matchingUser.email=j.get('email')
        session.flush()
        session.commit()
        return jsonify(
            {
                'id': matchingUser.id
            }
        )
    else:
        response = jsonify( {'message': 'User not found'} )
        response.status_code = 404
        return response


@app.route('/user', methods=['DELETE'])
def delete_user():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    userID = j.get('id')
    matchingUser = session.query(User).filter(User.id == userID).one_or_none()
    if matchingUser:
        session.delete(matchingUser)
        session.flush()
        session.commit()
        return jsonify(
            {
                'id': matchingUser.id
            }
        )
    else:
        response = jsonify( {'message': 'User not found'} )
        response.status_code = 404
        return response


@app.route('/club', methods=['GET'])
def get_club():

    schoolID = request.args.get('school_id')
    Session, engine = dbconnect(db_options)
    session = Session()
    clubs = session.query(Club).filter(Club.school_id == schoolID).all()
    ret_clubs = []
    for c in clubs:
        ret_clubs.append(
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'school_id': c.school_id,
            }
        )

    response = jsonify(ret_clubs)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/club', methods=['POST'])
def create_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    club = Club(
        name=j.get('name'),
        school_id=j.get('school_id'),
        description=j.get('description'),
    )
    session.add(club)
    session.flush()
    session.commit()
    return jsonify(
        {
            'id': club.id
        }
    )


@app.route('/club', methods=['PUT'])
def modify_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    clubID = j.get('id')
    matchingClub = session.query(Club).filter(Club.id == clubID).one_or_none()
    if matchingClub:
        if j.get('name') != None:
            matchingClub.name=j.get('name')
        if j.get('school_id') != None:
            matchingClub.school_id=j.get('school_id')
        if j.get('description') != None:
            matchingClub.description=j.get('description')

        session.flush()
        session.commit()
        return jsonify(
            {
                'id': clubID
            }
        )
    else:
        response = jsonify( {'message': 'Club not found'} )
        response.status_code = 404
        return response


@app.route('/club', methods=['DELETE'])
def delete_club():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    clubID = j.get('id')
    matchingClub = session.query(Club).filter(Club.id == clubID).one_or_none()
    if matchingClub:
        session.delete(matchingClub)
        session.flush()
        session.commit()
        return jsonify(
            {
                'id': clubID
            }
        )
    else:
        response = jsonify( {'message': 'Club not found'} )
        response.status_code = 404
        return response


@app.route('/schools', methods=['POST'])
def create_school():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    school_id = get_or_create_school(session, j['name'], j['address'])
    session.commit()
    return jsonify(
        {
            'id': school_id
        }
    )

@app.route('/schools', methods=['GET'])
def get_schools():
    Session, engine = dbconnect(db_options)
    session = Session()
    schools = session.query(School).all()
    #print schools
    formatted_schools = []
    for s in schools:
        formatted_schools.append({
            'name': s.name,
            'address': s.address
        })
    response = Response(json.dumps(formatted_schools))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/message', methods=['POST'])
def create_message():
    if request.mimetype != 'application/json':
        raise Exception('Content-Type is not "application/json".')
    j = request.get_json()
    Session, engine = dbconnect(db_options)
    session = Session()
    message = Message(
        club_id=j.get('club_id'),
        message=j.get('message')
    )
    session.add(message)
    session.flush()
    session.commit()
    return jsonify(
        {
            'id': message.id
        }
    )

@app.route('/message', methods=['GET'])
def get_message():
    club_id = request.args.get('club_id')
    Session, engine = dbconnect(db_options)
    session = Session()
    messages = session.query(Message).filter(Message.club_id == club_id).all()
    print (messages)
    ret_messages = []
    for m in messages:
        ret_messages.append(
            {
                'id': m.id,
                'club_id': m.club_id,
                'message': m.message
            }
        )

    response = Response(json.dumps(ret_messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    return send_from_directory(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static'),
        'index.html'
    )


if __name__ == '__main__':
    db_create(db_options)
    app.run(host='0.0.0.0', debug=True)