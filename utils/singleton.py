
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            print("Tworzenie instancji")
            instances[cls] = cls(*args, **kwargs)
        else:
            print("Zwracam istniejącą instancję")
        return instances[cls]

    return get_instance