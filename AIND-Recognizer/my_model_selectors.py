import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        best_model=None
        best_score=float("inf")

        for i in range(self.min_n_components,self.max_n_components+1):
            p= 2 * i * len(self.X[0])
            try:
                model_test=self.base_model(i).fit(self.X, self.lengths)
                model_score=-2 * model_test.score(self.X, self.lengths) + p * math.log(len(self.lengths))
                if model_score<best_score:
                    best_model=model_test
                    best_score=model_score
            except:
                pass
        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''
    def select(self):
        def get_other_score(model):
            '''Get the score of the model with other words
                return the score '''
            score=0
            len_others=0
            for w in self.words:
                if w != self.this_word:
                    X, lengths=self.hwords[w]
                    score = score  + model.score(X, lengths)
                    len_others=len_others + len(lengths)
            return  1 / (len_others) * score
        best_model=None
        best_score=float("-inf")
        for i in range(self.min_n_components,self.max_n_components+1):
            try:
                model_test=self.base_model(i).fit(self.X, self.lengths)
                model_score=model_test.score(self.X, self.lengths)
                model_score=model_score - get_other_score(model_test)
                if model_score>best_score:
                    best_model=model_test
                    best_score=model_score
            except Exception as inst:
                #print(inst)
                pass
        return best_model



class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''
    def select(self):
        def model_select_cross(i):
            '''For a (i)n_components choose the best model
                return the best model and it score '''
            split_method = KFold()
            best_model=None
            best_score=float("-inf")
            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                try:
                    X_train,lengths_train=combine_sequences(cv_train_idx, self.sequences)
                    X_test,lengths_test=combine_sequences(cv_test_idx, self.sequences)
                    model_test=self.base_model(i).fit(X_train,lengths_train)
                    model_score=model_test.score(X_test,lengths_test)
                    if model_score>best_score:
                        best_model=model_test
                        best_score=model_score
                except:
                    pass
            return best_model,best_score

        best_model=None
        best_score=float("-inf")
        for i in range(self.min_n_components,self.max_n_components+1):
            if (len(self.sequences))<3:
                # If we do not have enought sequences, fit and score with all secuences.
                try:
                    model_test=self.base_model(i).fit(self.X,self.lengths)
                    model_score=model_test.score(self.X,self.lengths)
                except:
                    model_score=float("-inf")
            else:
                model_test,model_score=model_select_cross(i)
            if model_score>best_score:
                best_model=model_test
                best_score=model_score
        return best_model

