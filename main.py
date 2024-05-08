from directory_creation import *
from parsing import *
from pipeline import Pipeline

pipeline = Pipeline("test_pipeline")

pipeline.load()
pipeline.execute()