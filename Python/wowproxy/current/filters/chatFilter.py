from .database import db

def chatFilter(data, env):
    # We received a chat message
    cursor = db.cursor()

    cursor.execute('INSERT INTO messages (message) VALUES (?)', (data.encode('hex'), ))
    db.commit()
