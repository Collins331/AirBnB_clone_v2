#!/usr/bin/python3
"""import Flask from flask"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """
    This function does not accept any argumemnt but
    return a block of text in a web page
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hello_hbnb():
    """
    Takes zero arguments but returns text
    thats rendered at /hbnb path
    """
    return "HBNB"


@app.route("/c/<text>")
def c_text(text):
    """
    Argument:
        text
    Return:
         a text begining with C and followed by argument passed
    """
    return "C {}".format(text.replace("_", " "))


@app.route("/python/", defaults={'text': 'is cool'})
@app.route("/python/<text>")
def python_text(text):
    """
    Argument:
        text with default value 'is cool'
    Return:
         a text begining with C and followed by argument passed
    """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number_int(n):
    """
    argurment:
        integer n
    Return:
        'n is a number' incase its integer
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    argurment:
        integer n
    Return:
        'n is a number' incase its integer
    """
    return render_template("5-number.html", number=n)


if __name__ == "__main__":
    """runs the app when the function is invorked"""
    app.run(host='0.0.0.0', port=5000)
