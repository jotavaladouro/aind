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



def recognize_gram(models: dict, test_set: SinglesData,n_gram=1,C=1,n_sentence_max=float("inf")):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    if (n_gram<1):
      probabilities,guesses=recognize(models,test_set)
      return  guesses

    def GetWordProbabilities(X, lengths ):
      retorno={}
      for word in models.keys():
        try:
          LogL = models[word].score(X, lengths)
        except:
          LogL=float("-inf")
        retorno[word]=LogL
      return retorno;
    def GetGramProbabilities(model_arp,key_list,lst_previo,eos_=False):
        #print("GetGramProbabilities : " + str(lst_previo))
        n_word_complete=(n_gram-1)
        if (len(lst_previo)>=n_word_complete):
          if (n_word_complete>0):
            if None not in lst_previo[-n_word_complete:]:
              string_gran= ' '.join(lst_previo[-n_word_complete:]) + " "
            else:
              string_gran= ''
          else:
            string_gran= ''
          sos_gran=False;
        else:
          if len(lst_previo)>0:
            string_gran=' '.join(lst_previo) + " "
          else:
            string_gran=""
          sos_gran=True;
        dict_retorno={}
        for word in key_list:
          test_gran=string_gran +  word
          try:
            dict_retorno[word]=model_arp.log_s(test_gran ,sos=sos_gran, eos=eos_)
          except:
            #print("GetGramProbabilities : except <" + word + "< " +  str(lst_previo) + "-->" + test_gran + "<")
            dict_retorno[word]=None
        key,minimo=min(dict_retorno.items())
        for word in key_list:
            if dict_retorno[word]==None:
              dict_retorno[word]=minimo
        #print(dict_retorno)
        return dict_retorno;

    def Guess(dict_word_p, dict_word_gram):
        retorno=None;
        p_retorno=float("-inf")
        for word in dict_word_p.keys():
          #print("Compare " + word + " " + str(dict_word_p[word]) + " " + str(dict_word_gram[word]))
            try:
              p= dict_word_p[word]+ C * dict_word_gram[word]
            except:
              p=dict_word_p[word]
            if p>p_retorno:
              retorno=word
              p_retorno=p

        return retorno;


    models_arpa = arpa.loadf("devel-lm-M3.sri.lm")
    model_arpa = models_arpa[0]
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    n_sentence=0
    for sentences_id in test_set.sentences_index:
      guesses_sentence=[]
      if n_sentence>=n_sentence_max:
        guesses = guesses  + [1] * (test_set.num_items - len(guesses))
        return guesses
      n_sentence=n_sentence +1
      for n in range(len(test_set.sentences_index[sentences_id])):
          word_id=test_set.sentences_index[sentences_id][n]
          if n==range(len(test_set.sentences_index[sentences_id])):
            eos_gram=True
          else:
            eos_gram=False
          #print("Word test " + str(word_id) )
          #print("Sentence " + str(sentences_id) + " index in sentence " + str(n) + " indice "  + str(word_id))
          X, lengths=test_set.get_item_Xlengths(word_id)
          dict_word_p=GetWordProbabilities(X, lengths)
          dict_word_p_gram=GetGramProbabilities(model_arpa,dict_word_p.keys(),guesses_sentence,eos_=eos_gram);
          guess=Guess(dict_word_p,dict_word_p_gram)
          guesses.append(guess)
          if guess==None:
            print("None guess " + str(sentences_id) + " " + str(n) + " " + str(guesses_sentence))
            print(dict_word_p)
            print(dict_word_p_gram)
          #print(guess)
          guesses_sentence.append(guess)
    return guesses



def recognize_gram_fix(models: dict, test_set: SinglesData,n_gram=1,C=1,n_sentence_max=float("inf")):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    if (n_gram<1):
      probabilities,guesses=recognize(models,test_set)
      return  guesses

    def GetWordProbabilities(X, lengths ):
      retorno={}
      for word in models.keys():
        try:
          LogL = models[word].score(X, lengths)
        except:
          LogL=float("-inf")
        retorno[word]=LogL
      return retorno;
    def GetGramProbabilities(model_arp,key_list,lst_previo,eos_=False):
        #print("GetGramProbabilities : " + str(lst_previo))
        n_word_complete=(n_gram-1)
        if (len(lst_previo)>=n_word_complete):
          if (n_word_complete>0):
            if None not in lst_previo[-n_word_complete:]:
              string_gran= ' '.join(lst_previo[-n_word_complete:]) + " "
            else:
              string_gran= ''
          else:
            string_gran= ''
          sos_gran=False;
        else:
          if len(lst_previo)>0:
            string_gran=' '.join(lst_previo) + " "
          else:
            string_gran=""
          sos_gran=True;
        dict_retorno={}
        for word in key_list:
          test_gran=string_gran +  word
          try:
            dict_retorno[word]=model_arp.log_s(test_gran ,sos=sos_gran, eos=eos_)
          except:
            #print("GetGramProbabilities : except <" + word + "< " +  str(lst_previo) + "-->" + test_gran + "<")
            dict_retorno[word]=None
        key,minimo=min(dict_retorno.items())
        for word in key_list:
            if dict_retorno[word]==None:
              dict_retorno[word]=minimo
        #print(dict_retorno)
        return dict_retorno;

    def Guess(dict_word_p, dict_word_gram):
        retorno=None;
        p_retorno=float("-inf")
        for word in dict_word_p.keys():
          #print("Compare " + word + " " + str(dict_word_p[word]) + " " + str(dict_word_gram[word]))
            try:
              p= dict_word_p[word]+ C * dict_word_gram[word]
            except:
              p=dict_word_p[word]
            if p>p_retorno:
              retorno=word
              p_retorno=p

        return retorno;


    models_arpa = arpa.loadf("devel-lm-M3.sri.lm")
    model_arpa = models_arpa[0]
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    n_sentence=0
    for sentences_id in test_set.sentences_index:
      guesses_sentence=[]
      if n_sentence>=n_sentence_max:
        guesses = guesses  + [1] * (test_set.num_items - len(guesses))
        return guesses
      n_sentence=n_sentence +1
      for n in range(len(test_set.sentences_index[sentences_id])):
          word_id=test_set.sentences_index[sentences_id][n]
          if n==range(len(test_set.sentences_index[sentences_id])):
            eos_gram=True
          else:
            eos_gram=False
          #print("Word test " + str(word_id) )
          #print("Sentence " + str(sentences_id) + " index in sentence " + str(n) + " indice "  + str(word_id))
          X, lengths=test_set.get_item_Xlengths(word_id)
          dict_word_p=GetWordProbabilities(X, lengths)
          dict_word_p_gram=GetGramProbabilities(model_arpa,dict_word_p.keys(),guesses_sentence,eos_=eos_gram);
          guess=Guess(dict_word_p,dict_word_p_gram)
          guesses.append(guess)
          if guess==None:
            print("None guess " + str(sentences_id) + " " + str(n) + " " + str(guesses_sentence))
            print(dict_word_p)
            print(dict_word_p_gram)
          #print(guess)
          guesses_sentence.append(guess)
    return guesses