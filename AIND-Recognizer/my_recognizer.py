import warnings
from asl_data import SinglesData
import arpa
import operator


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
      ''' For a secuence, return de probabilities of every word and
          the word with best score '''
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

    def get_gram_probabilities(lst_word,sos_func,eos_func):
        ''' Parameter: lst_word .- lista palabras
                        sos_func.- Start of sentence (bool)
                        eos_func .- End of sentence (bool)
            return a dictionary with a word and its gram probabilities'''
        dict_retorno={}
        for word in lst_word:
          try:
            if sos_func:
              if eos_func:
                  dict_retorno[word]=model_arpa.log_s(word)
              else:
                  dict_retorno[word]=model_arpa.log_s(word,eos=False)
            else:
              if eos_func:
                  dict_retorno[word]=model_arpa.log_s(word,sos=False)
              else:
                  dict_retorno[word]=model_arpa.log_s(word,eos=False,sos=False)

          except:
            dict_retorno[word]=None
        key,minimo=min(dict_retorno.items())
        for word in lst_word:
            if dict_retorno[word]==None:
              dict_retorno[word]=minimo
        return dict_retorno;

    def Guess(dict_word_p, dict_word_gram):
        ''' dict_word_p Dictionary with word and the visual probabilaties
            dict_word_gram Dictionary with word and the gram probabilaties
            retorno .- Word guesses'''
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
            eos_main=True
          probabilities_gram=get_gram_probabilities(models.keys(),sos_main,eos_main)
          guess=Guess(probabilities[word_id],probabilities_gram)
          guesses.append(guess)
    return guesses


def recognize_gram_2(models: dict, test_set: SinglesData,model_arpa,C=10):

    def get_gram_2_probabilities_total(eos_f=False):
        ''' Parameter: eos_f .- End of sentence (bool)
            return a dictionary with:
                  key: a list of 2  word
                  value its gram probabilities'''

        dict_retorno={}
        list_combine=[[word1,word2] for word1 in models.keys() for word2 in  models.keys() ]
        for (w1,w2) in list_combine:
          try:
            if eos_f:
              dict_retorno[(w1,w2)]=model_arpa.log_s(w1 + " " +w2)
            else:
              dict_retorno[(w1,w2)]=model_arpa.log_s(w1 + " " +w2 , eos=False)
            #print(str((w1,w2)) + " " + str(dict_retorno[(w1,w2)]) + "--" + w1 + " " +w2 )
          except Exception as e:
            #print(str((w1,w2)) + "-" + str(type(e)) + "-" + w1 + " " +w2 )
            dict_retorno[(w1,w2)]=None
        #print(dict_retorno)
        key,minimo=min(dict_retorno.items())
        for lst_words in dict_retorno.keys():
            if dict_retorno[lst_words]==None:
              dict_retorno[lst_words]=minimo
        return dict_retorno;

    def Guess_2_total(dict_word_p1,dict_word_p2,eos=False ):
        ''' dict_word_p1 Dictionary with word and the visual probabilaties for 1 word in sentence
            dict_word_p2 Dictionary with word and the visual probabilaties for 2 word in sentence
            eo .- End of sentence (bool)
            retorno .- word1,word2 guesses '''
        dict_word_gram=get_gram_2_probabilities_total( eos_f=eos)
        retorno=None;
        p_retorno=float("-inf")
        for (word1,word2) in dict_word_gram.keys():
            try:
              p= dict_word_p1[word1] +dict_word_p2[word2] + C * dict_word_gram[(word1,word2)]
            except:
              p= dict_word_p1[word1] +dict_word_p2[word2]
            if p>p_retorno:
              retorno=(word1,word2)
              p_retorno=p
        return retorno;
    def get_gram_probabilities(lst_words,eos_func,lst_prev):
        ''' Parameter: lst_word .- posible word list
                        eos_func .- End of sentence (bool)
                        lst_prev .- Previous word guesses
            return a dictionary with a word and its gram probabilities'''
        dict_retorno={}
        for word in lst_words:
          try:
            if (eos_func):
              dict_retorno[word]=model_arpa.log_s(lst_prev[-1] + " " +word)
            else:
              dict_retorno[word]=model_arpa.log_s(lst_prev[-1] + " " +word,eos=False)
          except:
            dict_retorno[word]=None
        key,minimo=min(dict_retorno.items())
        for word in lst_words:
            if dict_retorno[word]==None:
              dict_retorno[word]=minimo
        return dict_retorno;
    def Guess(dict_word_p, dict_word_gram):
        ''' dict_word_p Dictionary with word and the visual probabilaties
            dict_word_gram Dictionary with word and the gram probabilaties
            retorno .- Word guesses'''
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
      guesses_sentence=[]
      word_id1=test_set.sentences_index[sentences_id][0]
      word_id2=test_set.sentences_index[sentences_id][1]
      if len(test_set.sentences_index[sentences_id])==2:
        eos=True
      else:
        eos=False
      # Guess first 2 words of the sentence
      (first_gueses1,first_gueses2)=Guess_2_total(probabilities[word_id1],probabilities[word_id2])
      guesses.append(first_gueses1)
      guesses.append(first_gueses2)
      guesses_sentence.append(first_gueses1)
      guesses_sentence.append(first_gueses2)
      for n in range(2,len(test_set.sentences_index[sentences_id])):
          # Guess word by word
          word_id=test_set.sentences_index[sentences_id][n]
          eos_main=False
          if n==len(test_set.sentences_index[sentences_id]):
            eos_main=True
          probabilities_gram=get_gram_probabilities(models.keys(),eos_main,guesses_sentence)
          guess=Guess(probabilities[word_id],probabilities_gram)
          guesses.append(guess)
          guesses_sentence.append(guess)
    return guesses






def recognize_gram_3_only_best(models: dict, test_set: SinglesData,model_arpa,C=7,n_best=5):
    def str_from_lst(lst):
        if len(lst)==0:
          return ""
        retorno=lst[0]
        for k in lst[1:]:
          retorno=retorno + " " + k
        return retorno
    def get_gram_n_probabilities_total(list_combine):
        dict_retorno={}
        for word_lst in list_combine:
          try:
            dict_retorno[word_lst]=model_arpa.log_s(str_from_lst(word_lst), eos=False)
            #print(str((w1,w2)) + " " + str(dict_retorno[(w1,w2)]) + "--" + w1 + " " +w2 )
          except Exception as e:
            #print(str((w1,w2)) + "-" + str(type(e)) + "-" + w1 + " " +w2 )
            dict_retorno[word_lst]=None
        #print(dict_retorno)
        key,minimo=min(dict_retorno.items())
        for word_lst in dict_retorno.keys():
            if dict_retorno[word_lst]==None:
              dict_retorno[word_lst]=minimo
        return dict_retorno;

    def Guess_3_total(dict_word_p1,dict_word_p2,dict_word_p3):
        retorno=None;
        p_retorno=float("-inf")
        d1=dict(sorted(dict_word_p1.items(), key=operator.itemgetter(1), reverse=True)[:n_best])
        d2=dict(sorted(dict_word_p2.items(), key=operator.itemgetter(1), reverse=True)[:n_best])
        d3=dict(sorted(dict_word_p3.items(), key=operator.itemgetter(1), reverse=True)[:n_best])
        #print(d1)
        list_combine=[(word1,word2,word3) for word1 in d1.keys() for word2 in  d2.keys() for word3 in  d3.keys() ]
        dict_word_gram=get_gram_n_probabilities_total(list_combine)
        for (word1,word2,word3) in list_combine:
            try:
              p= dict_word_p1[word1] +dict_word_p2[word2] + dict_word_p3[word3] +  C * dict_word_gram[(word1,word2,word3)]
            except:
              p= dict_word_p1[word1] +dict_word_p2[word2] + dict_word_p3[word3]
            if p>p_retorno:
              retorno=(word1,word2,word3)
              p_retorno=p
        return retorno;

    def Guess_2_total(dict_word_p1,dict_word_p2,eos=False ):
        list_combine=[(word1,word2) for word1 in dict_word_p1.keys() for word2 in  dict_word_p2.keys() ]
        dict_word_gram=get_gram_n_probabilities_total(list_combine)
        retorno=None;
        p_retorno=float("-inf")
        for (word1,word2) in dict_word_gram.keys():
            try:
              p= dict_word_p1[word1] +dict_word_p2[word2] + C * dict_word_gram[(word1,word2)]
            except:
              p= dict_word_p1[word1] +dict_word_p2[word2]
            if p>p_retorno:
              retorno=(word1,word2)
              p_retorno=p
        return retorno;
    def get_gram_probabilities(eos_func,lst_prev):
        dict_retorno={}
        for word in models.keys():
          try:
            #print("get_gram_probabilities <" + str(lst_prev) +"> " + "<" + str(lst_prev[-2:]) +"> "+  str_from_lst(lst_prev[-2:]) + " " +word )
            if (eos_func):
              dict_retorno[word]=model_arpa.log_s(str_from_lst(lst_prev[-2:]) + " " +word)
            else:
              dict_retorno[word]=model_arpa.log_s(str_from_lst(lst_prev[-2:]) + " " +word,eos=False)
          except:
            dict_retorno[word]=None
        key,minimo=min(dict_retorno.items())
        for word in dict_retorno.keys():
            if dict_retorno[word]==None:
              dict_retorno[word]=minimo
        return dict_retorno;
    def Guess(dict_word_p,eos_f,guesses_sentence):
        retorno=None;
        p_retorno=float("-inf")
        dict_word_gram=get_gram_probabilities(eos_f,guesses_sentence)
        for word in dict_word_p.keys():
            try:
              p= dict_word_p[word]+ C * dict_word_gram[word]
              #print("Guess " + word +" "+ str(dict_word_p[word]) + " " + str(dict_word_gram[word]))
            except:
              p=dict_word_p[word]
              #print("Guess except" + word +" "+ str(dict_word_p[word]))
            if p>p_retorno:
              retorno=word
              p_retorno=p
        return retorno;
    def DoSentence(sentence_id,guesses):
      #print("DoSentence init")
      guesses_sentence=[]
      word_id1=test_set.sentences_index[sentences_id][0]
      word_id2=test_set.sentences_index[sentences_id][1]
      word_id3=test_set.sentences_index[sentences_id][2]
      (first_gueses1,first_gueses2,first_gueses3)=Guess_3_total(probabilities[word_id1],probabilities[word_id2],probabilities[word_id3])
      guesses.append(first_gueses1)
      guesses.append(first_gueses2)
      guesses.append(first_gueses3)
      guesses_sentence.append(first_gueses1)
      guesses_sentence.append(first_gueses2)
      guesses_sentence.append(first_gueses3)
      #print("DoSentence init " + str(guesses_sentence))
      for n in range(3,len(test_set.sentences_index[sentences_id])):
          word_id=test_set.sentences_index[sentences_id][n]
          eos_main=False
          if n==len(test_set.sentences_index[sentences_id]):
            eos_main=True
          guess=Guess(probabilities[word_id],eos_main,guesses_sentence)
          guesses.append(guess)
          guesses_sentence.append(guess)
    def DoSentence2(sentence_id,guesses):
        word_id1=test_set.sentences_index[sentences_id][0]
        word_id2=test_set.sentences_index[sentences_id][1]
        (first_gueses1,first_gueses2)=Guess_2_total(probabilities[word_id1],probabilities[word_id2])
        guesses.append(first_gueses1)
        guesses.append(first_gueses2)

    probabilities,guesses=recognize(models,test_set)
    guesses=[]
    for sentences_id in test_set.sentences_index:
        if len(test_set.sentences_index[sentences_id])>=3:
          DoSentence(sentences_id,guesses)
        else:
          DoSentence2(sentences_id,guesses)


    return guesses