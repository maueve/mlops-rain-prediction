from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('rain_prediction.html')

#if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(debug=False)