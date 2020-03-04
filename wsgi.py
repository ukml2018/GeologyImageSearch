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

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
charSet = "utf8mb4"

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
            apiKey = "Ja7s0jMglLzbrakE5h76OQUodSXpfVbNhKjT6dwS8WBt"
            version = "2020-02-29"
            visual_recognition = VisualRecognitionV3(version=version, iam_apikey=apiKey)
            with open(os.path.join(DATADIR, filename), 'rb') as images_file:
                classes = visual_recognition.classify(
                    images_file,
                    threshold='0.8',
                    classifier_ids='DefaultCustomModel_53113048').get_result()
            print(classes)
            data = (json.dumps(classes, indent=2))
            print('0')
            try:
               print('1')
               print(data)
               data = (data[data.index('"class": "') + 10:data.index(''"score"'') - 2]).rstrip()
               data = data[0:data.index('"')]
            except:
               print('In except block')
               #data = 'andesite'
               return render_template('index1.html')
            input =data
        print(input)
        image_names = os.listdir('./images/{}' .format(input))
        print(image_names)
        #print('3')
        if len(image_names) != 0:
               #print("4")
               return render_template("gallery.html", image_names=image_names)
    return render_template('index1.html')

@application.route('/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ =='__main__':
    application.run(debug = True)