from flask import Flask, render_template, request, redirect
import math

app = Flask(__name__)


def valid_number(number):
    # Only int values greater than 0 are allowed
    try:
        number_int = int(number)  # Convert from str to int
    except TypeError:
        return False
    if number_int <= 0:
        return False
    else:
        return True


def prime_number_check(number):
    if number == 1:  # 1 is not considered a prime number
        return False
    counter = 2
    while counter <= math.sqrt(number):
        if number % counter == 0:
            return False
        counter += 1
    return True


@app.route("/")
def index():
    return render_template("index.html")


# this is the function for submitting the number
@app.route("/submit", methods=["POST"])
def submit():
    input_number = request.form.get("number")
    if not valid_number(input_number):
        return redirect("/error")
    is_prime = prime_number_check(int(input_number))
    image_src = "happy.jpeg" if is_prime else "sad.jpeg"
    return render_template("prime_check.html", number=input_number,
                           is_prime=is_prime, image_src=image_src)


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/query")
def query():
    dinosaurs = request.ars.get('dinosaurs')
    if dinosaurs:
        return "Dinosaurs ruled the Earth 200 million years ago"
    
    asteroids = request.args.get('asteroids')
    if asteroids:
        return "Unkown"
