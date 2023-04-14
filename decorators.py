import time
import functools

def log(func):
    '''
    El siguiente decorador agrega un registro simple a una función.
    Cada vez que se llama a la función, se registra su nombre
    y la hora actual.
    '''
    def wrapper(*args, **kwgars):
        start_time = time.time()
        result = func(*args, **kwgars)
        end_time = time.time()
        print(f"Function {func.__name__} executed in {end_time - start_time} seconds")
        return result
    return wrapper

def cache(func):
    '''
    El siguiente decorador agrega caché a una función.
    Si la función se llama con los mismos argumentos varias veces,
    la caché almacena el resultado para evitar que la función
    se ejecute nuevamente.
    '''
    memory = {}
    def wrapper(*args):
        if args in memory:
            return memory[args]
        result = func(*args)
        memory[args] = result
        return result
    return wrapper

def requires_authentication(func):
    '''
    El siguiente decorador agrega autenticación a una función.
    Si la función se llama sin estar autenticado, se devuelve un error.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        is_authenticated = False
        if not is_authenticated:
            raise ValueError("User is not authenticated")
        is_authenticated = True
        return func(*args, **kwargs)
    return wrapper