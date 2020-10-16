from app import db


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    url = db.Column(db.String(100),nullable=False,unique=True)
    mimetype = db.Column(db.String(100),nullable=False)
    

    def __init__(self,name,url,mimetype):
        self.name = name
        self.url = url
        self.mimetype = mimetype
        

    def __repr__(self):
        return '<id {}>'.format(self.id)




