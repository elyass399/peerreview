from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy data for rooms and members
rooms = {}

@app.route('/')
def welcome_page():
    """
    Pagina di benvenuto.
    """
    return render_template('index.html')

@app.route('/join', methods=['GET', 'POST'])
def join_room():
    """
    Gestisce l'adesione a una stanza esistente.
    """
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        room_id = request.form['room_id']
        full_name = f"{first_name} {last_name}"
        session['user'] = full_name
        if room_id in rooms:
            rooms[room_id]['members'].append(full_name)
            rooms[room_id]['classement'][full_name] = 0  # Initialize score
            return redirect(url_for('room_page', room_id=room_id))
        else:
            return "Room ID not found", 404
    return render_template('join_room.html')

@app.route('/create', methods=['GET', 'POST'])
def create_room():
    """
    Gestisce la creazione di una nuova stanza.
    """
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        room_name = request.form['room_name']
        full_name = f"{first_name} {last_name}"
        session['user'] = full_name
        room_id = secrets.token_urlsafe(10)[:10]  # Generate a 10-character room ID
        rooms[room_id] = {'name': room_name, 'members': [full_name], 'classement': {full_name: 0}}
        return redirect(url_for('room_page', room_id=room_id))
    return render_template('create_room.html')

@app.route('/room/<room_id>')
def room_page(room_id):
    if room_id in rooms:
        members = rooms[room_id]['members']
        classement = rooms[room_id]['classement']
    else:
        members = []
        classement = {}
    return render_template('room.html', room_id=room_id, members=members, classement=classement)

@app.route('/personal_page')
def personal_page():
    # Placeholder for the personal page
    return "Pagina Personale"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
