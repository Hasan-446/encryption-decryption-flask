from flask import Flask,render_template,request,send_file
import hashlib
from Crypto.Cipher import AES
from werkzeug.utils import secure_filename
import os

#.\env\Scripts\activate.ps1
app = Flask(__name__)



basepath = os.path.dirname(__file__)
Upload_Folder = "uploads"
UPLOAD_PATH = os.path.join(basepath,Upload_Folder)
if not os.path.exists(UPLOAD_PATH):
    os.mkdir(UPLOAD_PATH)
        

def pad_msg(file): 
            while len(file)% 16 != 0:
                file = file + b'0'
            return file





@app.route('/')
def index():
    return render_template("index.html")


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method=="POST":
    
        file = request.files["file"]
        filename = file.filename
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,Upload_Folder,secure_filename(filename))
        _,ext = os.path.splitext(file_path)
        file.save(file_path)
        print(file_path)
        given_pass = request.form.get("pass")

        password=given_pass.encode("utf8")
        key=hashlib.sha256(password).digest()
        mode=AES.MODE_CBC
        iv="this is an iv456"

        cipher=AES.new(key,mode,iv.encode("utf8"))

        with open(file_path ,'rb') as f1:
            orig_file= f1.read()

        padded_file=pad_msg(orig_file)

        encrypted_msg=cipher.encrypt(padded_file)
        filename = "encrypted"+ext
        enc_file_path = os.path.join(basepath,Upload_Folder,filename)
        with open(enc_file_path, "wb") as f:
            f.write(encrypted_msg)
        
        #filename = filename.replace(" ","_")

        return render_template("encrypt.html",value=filename , download_button= True )
    
    return render_template("encrypt.html")



@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method=="POST":

        file = request.files["file"]
        filename = file.filename
       
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,Upload_Folder,secure_filename(filename))
        _, ext = os.path.splitext(file_path)
        file.save(file_path)
        print(file_path)
        given_pass = request.form.get("pass")

        password=given_pass.encode("utf8")
        key=hashlib.sha256(password).digest()
        mode=AES.MODE_CBC
        iv="this is an iv456"
        cipher=AES.new(key,mode,iv.encode("utf8"))

        with open(file_path ,'rb') as f1:
            orig_file= f1.read()

        decrypted_msg=cipher.decrypt(orig_file)

        filename = "decrypted"+ext
        dec_file_path = os.path.join(basepath,Upload_Folder,filename)

        with open(dec_file_path , "wb") as f:
            f.write(decrypted_msg)
        
        #filename = filename.replace(" ","_")

        return render_template("decrypt.html",value=filename, download_button= True)

    return render_template("decrypt.html")




    
@app.route('/<filename>')
def return_files_tut(filename):
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath,Upload_Folder,filename)
    return send_file(file_path, as_attachment=True, attachment_filename='')
        

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

