from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xaethei7raiTeeso@localhost/py_sweater'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

class MessageTagAssociation(db.Model):
    __tablename__ = 'message_tag_association'
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')



@app.route('/main', methods=['GET'])
def main():
    associations = MessageTagAssociation.query.all()
    messages_with_tags = []

    for association in associations:
        message = Message.query.get(association.message_id)
        tag = Tag.query.get(association.tag_id)
        messages_with_tags.append({'message': message.text, 'tag': tag.text})

    return render_template('main.html', messages_with_tags=messages_with_tags)



@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag_text = request.form['tag']
    tag = Tag.query.filter_by(text=tag_text).first()

    if not tag:
        tag = Tag(text=tag_text)
        db.session.add(tag)
        db.session.commit()

    message = Message(text=text)
    db.session.add(message)
    db.session.commit()

    association = MessageTagAssociation(message_id=message.id, tag_id=tag.id)
    db.session.add(association)
    db.session.commit()

    return redirect(url_for('main'))