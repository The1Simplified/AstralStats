from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
async def homepage():
    return render_template('homepage.html', title='Home')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
