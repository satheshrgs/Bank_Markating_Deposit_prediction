from flask import Flask, render_template, request, jsonify, send_file,url_for, Response
import os
from werkzeug import secure_filename
from model import createData
import pandas as pd

app= Flask(__name__)
@app.route('/')
def helloworld():
    return render_template('index.html')

@app.route('/result',methods=['POST','GET'])
def result():
        if request.method == 'POST':
                f = request.files['file']
                filename = secure_filename(f.filename)
                f.save(filename)

                bank = pd.read_csv(filename, sep = ',')
                output = createData(bank)

                return Response(
                    output.to_csv(),
                    mimetype="text/csv",
                    headers={"Content-disposition":
                             "attachment; filename=myplot.csv"})
                return render_template("sucess.html", name = f.filename)

@app.route('/download',methods = ['GET'])
def downloadFile():
        return send_file('test.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     attachment_filename='test.xlsx',
                     as_attachment=True)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
