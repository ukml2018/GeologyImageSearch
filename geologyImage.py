from flask import Flask,render_template, request, jsonify, redirect, flash, url_for, send_from_directory
import speech_recognition as sr
from flask_mysqldb import MySQL
import pymysql
import os
import yaml
from werkzeug.utils import secure_filename
import json
from watson_developer_cloud import VisualRecognitionV3
UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#app = Flask(__name__)
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
charSet = "utf8mb4"

#@app.route('/upload', methods=['GET', 'POST'])
@application.route('/', methods=['GET', 'POST'])
def find():
    #print(os.path)
    if request.method == 'POST':
        file = request.files['file']
        #print(type(file))
        if file.filename != '':
            filename = secure_filename(file.filename)
            #print(filename)
            SRCDIR = os.path.dirname(os.path.abspath(__file__))
            #print(SRCDIR)
            DATADIR = os.path.join(SRCDIR, 'images')
            #print(DATADIR)
            file.save(os.path.join(DATADIR, filename))
            #print('uploaded')
            apiKey = "vtrNuNjYNOQ82JmjBi7X0vmpsQT9jc5z7Nu9P6rWJv3h"
            version = "2020-01-16"
            visual_recognition = VisualRecognitionV3(version=version, iam_apikey=apiKey)
            with open(os.path.join(DATADIR, filename), 'rb') as images_file:
                classes = visual_recognition.classify(
                    images_file,
                    threshold='0.6',
                    classifier_ids='DefaultCustomModel_1149885701').get_result()
            data = (json.dumps(classes, indent=2))
            data = (data[data.index('"class": "') + 10:data.index(''"score"'') - 2]).rstrip()
            data = data[0:data.index('"')]
            input =data
        print(input)
        image_names = os.listdir('./images/{}' .format(input))
        print(image_names)
        if len(image_names) != 0:
               target = os.listdir('./images/{}' .format(input))
               if  os.path.isdir(target):
                  print(image_names)
                  return render_template("gallery.html", image_names=image_names)
               else :
                  print("This is a negative or unclassified image")
                  return render_template('index1.html')
    return render_template('index1.html')

@application.route('/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ =='__main__':
    application.run(debug = True)