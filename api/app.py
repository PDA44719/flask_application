from flask import Flask, render_template, request, redirect
import math
import numpy as np
import requests
from pydantic import BaseModel
import os


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


@app.route("/prime_check")
def prime_check():
    return render_template("prime_page.html")


# this is the function for submitting the number
@app.route("/prime_checked", methods=["POST"])
def prime_checked():
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


@app.route("/github_check")
def github_check():
    return render_template("github_check_page.html")


@app.route("/github", methods=["POST"])
def github():
    username = request.form.get("username")

    # Get all the public repo names
    url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(url)

    if repos_response.status_code != 200:
        return redirect("/github_error")
    repos = repos_response.json()
    if len(repos) == 0:
        return redirect("/github_no_user")

    repo_names = [repo["full_name"] for repo in repos]

    # Get the last commit of each repo
    list_of_last_commits = []
    for name in repo_names:
        url = f'https://api.github.com/repos/{name}/commits'
        commits_response = requests.get(url)
        commits = commits_response.json()
        try:
            list_of_last_commits.append(commits[0])  # append last commit

        except KeyError:  # no commits have been made in this repo
            list_of_last_commits.append("no commits")

    # Get all the required information for the table
    list_of_results = []
    for commit in list_of_last_commits:
        if commit == "no commits":
            d = {
                'hash': 'NONE',
                'author': 'NONE',
                'date': 'NONE',
                'message': 'NO COMMITS HAVE BEEN MADE'
            }
        else:
            d = {
                'hash': commit['sha'][:7],
                'author': commit['commit']['author']['email'],
                'date': commit['commit']['author']['date'][:10],
                'message': commit['commit']['message']
            }
        list_of_results.append(d)
    return render_template("github.html", username=username, repos=repo_names,
                           commit_results=list_of_results)


@app.route("/github_error")
def github_error():
    return render_template("github_error.html")


@app.route("/github_no_user")
def github_no_user():
    return render_template("github_no_user.html")


@app.route("/nasa")
def nasa():
    return render_template("nasa.html", explanation="", url="")


@app.route("/nasa", methods=["POST"])
def nasa_form_and_picture():
    year = request.form.get("year")
    month = request.form.get("month")
    day = request.form.get("day")

    if len(month) < 2:
        month = '0' + month
    if len(day) < 2:
        day = '0' + day

    date = f'{year}-{month}-{day}'

    # define the base url and the parameters
    base_url = "https://api.nasa.gov/planetary/apod?"
    query_parameters = {
        "date": date,
        "api_key": "60vSeyurGsbd9hhIGpvOo1QS9istjh8vmKsHaqSo"
    }

    # obtain the picture of the day, at the specified date
    pic_of_the_day = requests.get(base_url, params=query_parameters)
    if pic_of_the_day.status_code == 200:
        pic_of_the_day = pic_of_the_day.json()
        explanation = pic_of_the_day['explanation']
        url = pic_of_the_day['url']
    else:
        explanation = ''
        url = ''
    return render_template("nasa.html", explanation=explanation, url=url)

