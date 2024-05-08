from directory_creation import *
from parsing import *
from pipeline import Pipeline

pip = Pipeline('test_pipeline')

pip.load()

pip.execute()
