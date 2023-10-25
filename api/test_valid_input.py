from app import valid_number


def test_valid():
    valid_numbers_list = [str(number) for number in range(1, 21)]
    non_valid_numbers_list = ['-5', 'a', '10.7']

    for number in valid_numbers_list:
        assert valid_number(number) is True

    for number in non_valid_numbers_list:
        assert valid_number(number) is False
