from nlu_helper.read_model import MatrixModel
from nlu_helper.read_model import SentenceProcessor
import os


class Similarity:
    def __init__(self):
        # the file path has the resources folder as a reference
        # filepaths are relative to the resources folder of the nlu_helper module
        model_filename = 'all_senate_speeches_stop_tfidf_svd100_lsa_49934x150'

        self.sp = SentenceProcessor(MatrixModel(model_filename))

    def similarity(self, real_answer : str, given_answer : str):
        return self.sp.get_sentence_match(real_answer, given_answer)
