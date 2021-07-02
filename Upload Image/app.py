from flask import Flask,render_template,request,flash,redirect,url_for
import os
import sqlite3

app=Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("myimage.db")
con.execute("create table if not exists image(pid integer primary key,img TEXT)")
con.close()

app.config['UPLOAD_FOLDER']="static\images"

@app.route("/",methods=['GET','POST'])
def upload():

    con = sqlite3.connect("myimage.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from image")
    data = cur.fetchall()
    con.close()

    if request.method=='POST':
        upload_image=request.files['upload_image']

        if upload_image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            con=sqlite3.connect("myimage.db")
            cur=con.cursor()
            cur.execute("insert into image(img)values(?)",(upload_image.filename,))
            con.commit()
            flash("File Upload Successfully","success")

            con = sqlite3.connect("myimage.db")
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("select * from image")
            data=cur.fetchall()
            con.close()
            return render_template("upload.html",data=data)
    return render_template("upload.html",data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=sqlite3.connect("myimage.db")
        cur=con.cursor()
        cur.execute("delete from image where pid=?",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("upload"))
        con.close()

if __name__ == '__main__':
    app.run(debug=True)