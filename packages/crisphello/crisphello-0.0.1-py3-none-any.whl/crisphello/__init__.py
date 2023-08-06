
def hello(name=None):
    if name is None:
        return "Hello world!"
    else:
        return f'Hello, {name}!'

def add(num1, num2):
    return num1 + num2