

def some_code():
    # something complicated goes here
    pass


class MyException(Exception):
    pass

# Worst way:
try:
    some_code()
except Exception as err:
    print("It's bad!")


# Good way:
try:
    some_code()
except MyException as err1:
    pass  # do something useful here
except ValueError as err2:
    pass  # do something useful here
