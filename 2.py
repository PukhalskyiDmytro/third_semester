import random
from datetime import datetime

# task 1
def mask_password(cls):
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


# task 2
def exception_logger(cls):
    def make_wrapper(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                with open("errors.log", "a", encoding="utf-8") as f:
                    f.write(
                        f"[{datetime.now()}] "
                        f"Error in {cls.__name__}.{func.__name__} "
                        f"args={args}, kwargs={kwargs}, error={e}\n"
                    )
                return None

        return wrapper

    for name, attr in cls.__dict__.items():
        if callable(attr):
            setattr(cls, name, make_wrapper(attr))

    return cls


@exception_logger
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.items:
            raise IndexError("Черга порожня!")
        return self.items.pop(0)

    def __len__(self):
        return len(self.items)


def simulate(m=3, t1=3, t2=5, T=30):
    queue = Queue()

    for i in range(1, m + 1):
        queue.enqueue(f"Buyer{i}")

    time_service = random.randint(1, t1)
    time_add = random.randint(1, t2)

    for t in range(1, T + 1):
        if t == time_service:
            buyer = queue.dequeue()
            print(f"{t}: Обслуговування {buyer}")
            time_service = t + random.randint(1, t1)

        if t == time_add:
            new_buyer = f"Buyer_{t}"
            queue.enqueue(new_buyer)
            print(f"{t}: Додано {new_buyer}")
            time_add = t + random.randint(1, t2)

    print("\nЗалишок у черзі:", len(queue))
    print("Черга:", queue.items)


# task 3
class CatchErrorsMeta(type):
    def __new__(mcs, cls_name, bases, namespace):
        def build_guard(func):
            def guarded(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    with open("errors.log", "a", encoding="utf-8") as f:
                        f.write(
                            f"[{datetime.now()}] "
                            f"Error in {cls_name}.{func.__name__} "
                            f"args={args}, kwargs={kwargs}, error={e}\n"
                        )
                    return None

            return guarded

        for method_name, method in namespace.items():
            if callable(method):
                namespace[method_name] = build_guard(method)

        return super().__new__(mcs, cls_name, bases, namespace)


class CustomerQueue(metaclass=CatchErrorsMeta):
    def __init__(self):
        self._storage = []

    def add_customer(self, customer):
        self._storage.append(customer)

    def serve_customer(self):
        if not self._storage:
            raise IndexError("Черга порожня!")
        return self._storage.pop(0)

    def __len__(self):
        return len(self._storage)


def simulate_meta(m=3, t1=3, t2=5, T=30):
    queue = CustomerQueue()
    for i in range(1, m + 1):
        queue.add_customer(f"Buyer{i}")

    next_service = random.randint(1, t1)
    next_add = random.randint(1, t2)

    for t in range(1, T + 1):
        if t == next_service:
            buyer = queue.serve_customer()
            print(f"{t}: Обслуговування {buyer}")
            next_service = t + random.randint(1, t1)

        if t == next_add:
            new_buyer = f"Buyer_{t}"
            queue.add_customer(new_buyer)
            print(f"{t}: Додано {new_buyer}")
            next_add = t + random.randint(1, t2)

    print("\nЗалишок у черзі:", len(queue))
    print("Черга:", queue._storage)


if __name__ == "__main__":
    # task 1
    u = User("andriy", "secret")
    print(u)
    # task 2
    simulate(m=3, t1=5, t2=4, T=50)
    # task 3
    simulate_meta(m=3, t1=5, t2=4, T=50)
