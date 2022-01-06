from flask import Flask, render_template

app = Flask(__name__)

# instructions can be found in the README.md file.
# this is the file that has to be run in order to begin execution of the program


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/about/")
def about():
    return str(open('coverletter2021.txt', 'r').readlines())



if __name__ == '__main__':
    app.run()
