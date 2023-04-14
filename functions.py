import time
from decorators import (
    log,
    cache,
    requires_authentication
)

@log
def test_log():
    time.sleep(2)
    print("Hello, World!")

#test_log()

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

#print(fibonacci(50))

@requires_authentication
def secret_function():
    print("This is a secret function")

secret_function()