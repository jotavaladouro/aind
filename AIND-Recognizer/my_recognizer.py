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



def recognize_gram(models: dict, test_set: SinglesData,n_gram=1):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    C=25
    if (n_gram<1):
      return recognize(models,test_set)

    def GetWordProbabilities(X, lengths ):
      retorno={}
      for word in models.keys():
        try:
          LogL = models[word].score(X, lengths)
        except:
          LogL=float("-inf")
        retorno[word]=LogL
      return retorno;
    def GetGramProbabilities(model_arp,key_list,lst_previo=None):
        dict_retorno={}
        for word in key_list:
          try:
            dict_retorno[word]=model_arp.log_s(word,sos=False, eos=False)
          except:
            dict_retorno[word]=0
        return lst_retorno;

    def Guess(dict_word_p, dict_word_gram):
        retorno=None;
        p_retorno=float("-inf")
        for word in dict_word_p.keys():
          p= dict_word_p[word]+ C * dict_word_gram[word]
          if p>p_retorno:
            retorno=word
            p_retorno=p

        return retorno;


    models_arpa = arpa.loadf("devel-lm-M3.sri.lm")
    model_arpa = models_arpa[0]
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    for sentences_id in test_set.sentences_index:
      for n in range(len(test_set.sentences_index[sentences_id])):
          word_id=test_set.sentences_index[sentences_id][n]
          X, lengths=test_set.get_item_Xlengths(word_id)
          dict_word_p=GetWordProbabilities(X, lengths)
          dict_word_p_gram=GetGramProbabilities(model_arp,dict_word_p.keys());
          guesses.append(Guess(dict_word_p,dict_word_p_gram))
    return guesses
