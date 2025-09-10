#task 1
def mask_password(cls):
    orig_repr = cls.__repr__ if "__repr__" in cls.__dict__ else None

    def new_repr(self):
        attrs = []
        for k, v in self.__dict__.items():
            if k == "password":
                v = "*" * len(str(v))
            else:
                v = repr(v)
            attrs.append(f"{k}={v}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    cls.__repr__ = new_repr
    return cls

@mask_password
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

u = User("andriy", "mysecret")
print(u)
