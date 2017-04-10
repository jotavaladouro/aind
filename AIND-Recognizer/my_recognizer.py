import warnings
from asl_data import SinglesData
import arpa


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """

    def GetProbabilities(X, lengths ):
      retorno={}
      word_guesses=None
      word_guesses_logL=float("-inf")
      for word in models.keys():
        try:
          LogL = models[word].score(X, lengths)
        except:
          LogL=float("-inf")
        retorno[word]=LogL
        if LogL>word_guesses_logL:
          word_guesses=word
          word_guesses_logL=LogL
      return retorno,word_guesses;


    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    for n in range(test_set.num_items) :
      X, lengths=test_set.get_item_Xlengths(n)
      dict_retorno,word_guesses=GetProbabilities(X, lengths )
      probabilities.append(dict_retorno);
      guesses.append(word_guesses)
    return probabilities,guesses


def recognize_gram_1(models: dict, test_set: SinglesData,model_arpa,C=7):

    def get_gram_probabilities(models: dict,sos_func,eos_func):
        dict_retorno={}
        for word in models.keys():
          try:
            dict_retorno[word]=model_arpa.log_s(word ,sos=sos_func, eos=eos_func)
          except:
            dict_retorno[word]=None
        key,minimo=min(dict_retorno.items())
        for word in models.keys():
            if dict_retorno[word]==None:
              dict_retorno[word]=minimo
        return dict_retorno;

    def Guess(dict_word_p, dict_word_gram):
        retorno=None;
        p_retorno=float("-inf")
        for word in dict_word_p.keys():
            try:
              p= dict_word_p[word]+ C * dict_word_gram[word]
            except:
              p=dict_word_p[word]
            if p>p_retorno:
              retorno=word
              p_retorno=p
        return retorno;

    probabilities,guesses=recognize(models,test_set)
    guesses=[]
    for sentences_id in test_set.sentences_index:
      for n in range(len(test_set.sentences_index[sentences_id])):
          word_id=test_set.sentences_index[sentences_id][n]
          sos_main=False
          eos_main=False
          if (n==0):
            sos_main=True
          if n==len(test_set.sentences_index[sentences_id]):
            eos_main=False
          probabilities_gram=get_gram_probabilities(models,sos_main,eos_main)
          guess=Guess(probabilities[word_id],probabilities_gram)
          guesses.append(guess)
    return guesses


def recognize_gram_2(models: dict, test_set: SinglesData,model_arpa,C=7):

    def get_gram_2_probabilities_total(models: dict,sos_func,eos_func):
        dict_retorno={}
        list_combine=[[word1,word2] for word1 in models.keys() for word2 in  models.keys() ]
        for lst_words in list_combine:
          try:
            dict_retorno[lst_words]=model_arpa.log_s(lst_words ,sos=sos_func, eos=eos_func)
          except:
            dict_retorno[lst_words]=None
        key,minimo=min(dict_retorno.items())
        for lst_words in dict_retorno.keys():
            if dict_retorno[lst_words]==None:
              dict_retorno[lst_words]=minimo
        return dict_retorno;

    def Guess_2_total(dict_word_p1,dict_word_p2, dict_word_gram):
        retorno=None;
        p_retorno=float("-inf")
        for word in dict_word_p.keys():
            try:
              p= dict_word_p[word]+ C * dict_word_gram[word]
            except:
              p=dict_word_p[word]
            if p>p_retorno:
              retorno=word
              p_retorno=p
        return retorno;

    probabilities,guesses=recognize(models,test_set)
    guesses=[]
    for sentences_id in test_set.sentences_index:

      for n in range(len(test_set.sentences_index[sentences_id])):
          word_id=test_set.sentences_index[sentences_id][n]
          sos_main=False
          eos_main=False
          if (n==0):
            sos_main=True
          if n==len(test_set.sentences_index[sentences_id]):
            eos_main=False
          probabilities_gram=get_gram_probabilities(models,sos_main,eos_main)
          guess=Guess(probabilities[word_id],probabilities_gram)
          guesses.append(guess)
    return guesses