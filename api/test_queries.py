from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == "Dinosaurs ruled"\
            + " the Earth 200 million years ago"


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_name():
    assert process_query("What is your name?") == "Pablo&Gabriel"


def test_addition():
    assert process_query("What is 53 plus 27?") == "80"


def test_largest():
    query = "Which of the following numbers is the largest: 23, 47, 11?"
    assert process_query(query) == "47"


def test_square_cube():
    query_part1 = "Which of the following numbers is both a square and "
    query = query_part1 + "a cube: 1, 2, 3, 4, 5, 7, 64?"
    assert process_query(query) == "64"


def test_multiply():
    query = "What is 12 multiplied by 2?"
    assert process_query(query) == "24"
