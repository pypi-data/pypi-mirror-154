from .dict import DictDatabase
try:
    from .mongo import MongoDatabase
except ModuleNotFoundError:
    pass

