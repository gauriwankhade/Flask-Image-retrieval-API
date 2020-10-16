import os
from flask import Flask,render_template, request
from werkzeug.utils import secure_filename 

from db import db_init,db
from models import Images
from PIL import Image


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_user:Gauri@007@localhost/mynewdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'the random string'  
db_init(app)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# change image dimensions to 1000*1000
def resize_file(file):
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    image = Image.open(file)
    new_image = image.resize((1000,1000),Image.ANTIALIAS)
    new_image.save(path,quality=95)
    print(new_image)
    

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files:
            return ("No File uploaded"),400
        if file.name == '':
            return ("No File Selected"),400
        if file and allowed_file(file.filename):
            
            if Images.query.filter_by(name=file.filename).first()!= None:
                return ("file already exists")
            else:
                resize_file(file) #resize image
                
                filename = secure_filename(file.filename)
                mimetype = filename.split('.')[1]
                url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img=Images(name=filename,url=url,mimetype=mimetype)

                db.session.add(img)
                db.session.commit() # saved image data in database

                return ("successs"),200
        else:
        	return ("Please enter valid input"),400

    return render_template('index.html')
      
@app.route('/uploads/<id>')
def uploaded_file(id):   
    if(Images.query.get(id)) :
        img = Images.query.get(id)
       	return render_template('upload.html',img=img)
    else:
       	return ("image not found",404)
    
    


if '__name__'=='__main__':

	app.run(debug=True)








