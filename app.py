from flask import Flask, request, jsonify, render_template
from textsummarizer import *
from webpagesummary import *
from documentsummary import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize',methods=['POST'])
def summarize():

    if request.method == 'POST':

        text = request.form['originalText']
        if not request.form['numOfLines']:
            numOfLines = 3
        else:
            numOfLines = int(request.form['numOfLines'])

        summary, original_length = generate_summary(text,numOfLines)

        return render_template('result.html',
                               text_summary=summary,
                               lines_original = original_length,
                               lines_summary = numOfLines)


@app.route('/summarize2',methods=['POST'])
def summarize2():

    if request.method == 'POST':

        lnk = request.form['webpage_link']

        summary, original_length, numOfLines = generate_summary2(lnk)

        return render_template('result.html',
                               text_summary=summary,
                               lines_original = original_length,
                               lines_summary = numOfLines)

@app.route('/summarize3',methods=['POST'])
def summarize3():

    if request.method == 'POST':

        file=request.files['file']
        if file:
            file.save(file.filename)
        summary,original_length,numOfLines=generate_summary3(file)
        return render_template('result.html',
                               text_summary=summary,
                               lines_original = original_length,
                               lines_summary = numOfLines)


@app.route("/web_page_summarizer")
def test_link():
    return render_template('web_page_summarizer.html')


@app.route("/text_summarizer")
def test_link2():
    return render_template('text_summarizer.html')


@app.route("/document_summarizer")
def test_link3():
    return render_template('document_summarizer.html')

if __name__ == '__main__':
    app.run(debug=True)
