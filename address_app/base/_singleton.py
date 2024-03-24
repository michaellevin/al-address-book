# * Singleton classes
class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def delete_instance(cls):
        cls._instance = None
