from flask import Flask, render_template, request
import math

app = Flask(__name__)

def prime_number_check(number):
    counter = 2
    while counter <= math.sqrt(number):
        if number % counter == 0:
            return False
        counter += 1
    return True


@app.route("/")
def hello_world():
    return render_template("index.html") 

#this is the function for submitting the number
@app.route("/submit", methods=["POST"])
def submit():
    input_number = request.form.get("number")
    is_prime = prime_number_check(int(input_number))
    image_src = "happy.jpeg" if is_prime else "sad.jpeg"
    return render_template("prime_check.html", number=input_number, is_prime=is_prime, image_src=image_src) 
