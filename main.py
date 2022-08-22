from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SECRET_KEY'] = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id')) # POSSIBLY CAN BE NULL
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # CANNOT BE NULL
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id')) # CAN BE NULL
    replies = db.relationship('Comment') # NOT PARENT! ITS REPLIES, add to parent by root.replies.append([<Comment (reply) >])

# SERIALIZERS
class CommentSerializer(ma.Schema):
    class Meta:
        fields = [
            'content',
            'post_id',
            'user_id',
            'parent_id',
            'replies'
        ]

    replies = ma.Nested('CommentSerializer', many=True)

class PostSerializer(ma.Schema):
    class Meta:
        fields = [
            'content',
            'user_id',
            'comments'
        ]

    comments = ma.Nested(CommentSerializer, many=True)

class UserSerializer(ma.Schema):
    class Meta:
        fields = [
            'username',
            'posts'
        ]

    posts = ma.Nested(PostSerializer, many=True)

# VIEWS
@app.route('/')
def index():
    user = User.query.get(1)
    post = Post.query.get(1)
    print(user)
    print(user.posts)
    print(post.comments)
    print("replies: ", post.comments[0].replies)
    return {'user': UserSerializer().dump(user)}

if __name__ == "__main__":
    app.run(debug=True)

