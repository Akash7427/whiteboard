# -*- coding: utf-8 -*-
# @Author: amish
# @Date:   2021-04-15 18:54:48
# @Last Modified by:   amish
# @Last Modified time: 2021-04-15 19:58:06

from flask import Flask, render_template, request, jsonify, url_for, abort
from modules import main
import requests,  os, cv2
from werkzeug.utils import secure_filename
from google.cloud import storage
#from firebase import firebase


app = Flask(__name__)

@app.route('/', methods=['POST'])



def home():
	file = request.files['file']
	if file:
		filename = secure_filename(file.filename)
		credfilename = secure_filename("credentials.json")
		file.save(os.path.join("./uploaded_images", filename))
		flag, sharpen_image = main.main_func(filename)
		
		if flag == False:
			return jsonify({"response": "This image cannot be detected!!"})
		else:
			cv2.imwrite(os.path.join("./output_images" , filename), sharpen_image)
			os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join("./",credfilename)
			#firebase = firebase.FirebaseApplication('<your firebase database path>')
			client = storage.Client()
			bucket = client.get_bucket('whiteboard-digitization.appspot.com')
			imageBlob = bucket.blob("/")
			imagePath = os.path.join("./output_images" , filename)
			imageBlob = bucket.blob(filename)
			imageBlob.upload_from_filename(imagePath)
			imageBlob.make_public()
			print(imageBlob.public_url)
			return jsonify(imageBlob.public_url)
			#return jsonify({"response": "Processed image saved at ./output_images!!"})

if __name__ == '__main__':
	app.run(debug=False,host='192.168.2.6',port=5555)
	server.run(debug=False,host='192.168.2.6',port=5555)