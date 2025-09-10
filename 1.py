#task 1
def invert_sign(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)    
        return -result                   
    return wrapper

@invert_sign
def sum(a: int , b: int ):
    return a + b
    
print(sum(5,2))

#task 2
def from_a_to_b(a:float, b:float):
    def _from_a_to_b(func):
        def __from_a_to_b(x1, x2, *args, **kwargs):
            x1 = max(a, min(x1, b))
            x2 = max(a, min(x2, b))
            result = func(x1, x2, *args, **kwargs)
            return result
        return __from_a_to_b
    return _from_a_to_b
    
@from_a_to_b(1,3)
def get_numbers(x1: float, x2:float):
    return x1, x2
    
print(get_numbers(-2, -2))

#task 3
def without_repitition(func):
    def _without_repitition(*args, **kwargs):
        result = func(*args, **kwargs)
        result = list(set(result))
        return result
    return _without_repitition

@without_repitition 
def get_words_from_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    return words
    
print(get_words_from_file("1.txt"))
