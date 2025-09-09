def invert_sign(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)    
        return -result                   
    return wrapper

@invert_sign
def sum(a: int , b: int ) -> int:
    return a + b
    
print(sum(5,2))

def from_a_to_b(a:float, b:float):
    def _from_a_to_b(func):
        def __from_a_to_b(*args, **kwargs):
            result = func(*args, **kwargs)
            result = max(a, min(result, b))
            return result
        return __from_a_to_b
    return _from_a_to_b
    
@from_a_to_b(1,3)
def get_number(a: float):
    return a
    
print(get_number(-2))

def without_repitition(func):
    def _without_repitition(*args, **kwargs):
        result = func(*args, **kwargs)
        result = list(set(result))
        return result
    return _without_repitition

@without_repitition 
def get_list(l):
    return l
    
print(get_list([1,1,1,2,5]))

            
