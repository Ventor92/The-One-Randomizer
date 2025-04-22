
def singleton(cls):
    instance = None

    def custom_new(cls_, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = super(cls_, cls_).__new__(cls_)  # poprawne wywołanie object.__new__
            cls_.__init__(instance, *args, **kwargs)    # ręczne wywołanie __init__
            print(f"Tworzenie instancji {instance.__class__.__name__}")
        else:
            print(f"Zwracam istniejącą instancję {instance.__class__.__name__}") 
            
        return instance

    cls.__new__ = staticmethod(custom_new)
    return cls