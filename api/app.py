from flask import Flask, render_template, request, redirect
import math
import numpy as np
import requests

app = Flask(__name__)


def valid_number(number):
    # Only int values greater than 0 are allowed
    try:
        number_int = int(number)  # Convert from str to int
        print(number_int)
    except (TypeError, ValueError):
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


def addition(query):
    query_split = query.split()
    num1 = int(query_split[2])
    num2 = int(''.join([char for char in query_split[4] if char != "?"]))
    return str(num1 + num2)


def highest_of_three_values(query):
    query_split = query.split()
    num1 = int(query_split[-1][:-1])
    num2 = int(query_split[-2][:-1])
    num3 = int(query_split[-3][:-1])
    return str(max(num1, num2, num3))


def square_and_cube(query):
    query_split = query.split()
    num1 = int(query_split[-1][:-1])
    num2 = int(query_split[-2][:-1])
    num3 = int(query_split[-3][:-1])
    num4 = int(query_split[-4][:-1])
    num5 = int(query_split[-5][:-1])
    num6 = int(query_split[-6][:-1])
    num7 = int(query_split[-7][:-1])
    num_list = [num1, num2, num3, num4, num5, num6, num7]
    for num in num_list:
        if num == 729:
            print(math.sqrt(num) % 1)
            print(round(np.cbrt(num) % 1, 100))
        if math.sqrt(num) % 1 == 0 and np.cbrt(num) % 1 == 0:
            return str(num)
    return ""  # No number found


def multiply(query):
    query_split = query.split()
    num1 = int(query_split[2])
    num2 = int(query_split[5][:-1])
    return str(num1 * num2)


def process_query(query):
    if query == 'dinosaurs':
        return "Dinosaurs ruled the Earth 200 million years ago"
    if query == 'asteroids':
        return "Unknown"
    if "name" in query:
        return "Pablo&Gabriel"
    if "plus" in query:
        return addition(query)
    if "the largest:" in query:
        return highest_of_three_values(query)
    if "square" in query and "cube" in query:
        return square_and_cube(query)
    if "multiplied by" in query:
        return multiply(query)
    return "Invalid query"


@app.route("/query")
def query():
    query = request.args.get('q')
    return process_query(query)


@app.route("/github", methods=["POST"])
def github():
    username = request.form.get("username")
    print(username)
    # Get repos response
    repos_response = requests.get(f'https://api.github.com/users/{username}/repos')
    print(repos_response)
    if repos_response.status_code == 200:
        # data returned is a list of ‘repository’ entities
        repos = repos_response.json()
        repo_names = []
        for repo in repos:
            repo_names.append(repo["full_name"])

    # Get the commits of each repo
    for name in repo_names:
        commits_response = requests.get(f'https://api.github.com/repos/{name}/commits')
        commits = commits_response.json()
        print([commit for commit in commits])
        print("\n\n")
    return render_template("github.html", username=username, repos=repo_names)
