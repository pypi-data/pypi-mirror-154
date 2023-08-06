from typing import Optional
import re
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from .konlpy_mecab import KnlyMD


class KeywordFactory:
    """
    Classification based sentiment analysis using Review Corpus

    Examples:
        >>> key = package(task="keyword", model= model_path )
        >>> key("배송이 버트 학습시키는 것 만큼 느리네요")
        [('버트', 0.4204), ('느리네요', 0.3776), ('학습', 0.3342), ('배송', 0.3068)]
        >>> key("배송이 버트 학습시키는 것 만큼 느리네요", topn=5, nlpmode ='post',kwmode='maxsum') #nlpmode='noun','post' /kwmode='maxsum' or 'use_mmr' or orgin
        [('버트', 0.4204), ('느리네요', 0.3776), ('학습', 0.3342), ('배송', 0.3068)]
    """

    def __init__(self, model: Optional[str],**kwargs):

        if model is None:
            model_path = self.get_available_models()["klue_base"]
        else:
            model_path = model

        sentence_model = SentenceTransformer(model_path)
        kw_model = KeyBERT(model=sentence_model)
        self.kw_model = kw_model

    @staticmethod
    def get_available_models():
        return {
            "klue_base":
                'samba/samba-large-bert-fine-tuned'

        }

    def __call__(self, sent: str, **kwargs): # package의 인스턴스를 인스터스화 했을때 호출
        # print("Factory에 __call__ 호출")
        return self.predict(sent, **kwargs)


    def predict(self, sent:str,  **kwargs ): # nlpmode='noun','post' /kwmode='maxsum' or 'use_mmr' or orgin

        topn = kwargs.get("topn", 10) #defalt topn = 10개
        nlpmode = kwargs.get("nlpmode", 'post') #defalt nlpmode = 'post'
        kwmode = kwargs.get("nlpmode", None) #defalt kwmode = None

        if nlpmode == 'noun': sent = ', '.join(KnlyMD.pos_tagger(sent, 'noun'))

        if kwmode == 'maxsum':
            #Max Sum Similarity
            keywords = self.kw_model.extract_keywords(sent, keyphrase_ngram_range=(1, 1), stop_words=None,
                                                use_maxsum=True, nr_candidates=20, top_n=topn)
        elif kwmode == 'use_mmr':
            #Maxinal Marginal Relevance
            keywords = self.kw_model.extract_keywords(sent, keyphrase_ngram_range=(1, 1), stop_words=None,
                                            use_mmr=True, diversity=0.7,top_n=topn) #high diversity
        else :
            keywords = self.kw_model.extract_keywords(sent, keyphrase_ngram_range=(1, 1), stop_words=None,
                                                top_n=topn)

            keywords.sort(key=lambda x: x[1], reverse=True)
            keywords = list(filter(lambda x: x[1] >= 0.15, keywords))
            if nlpmode == 'post':
                sent = sent.center(len(sent)+2)
                sent = sent.upper()

                units = KnlyMD.pos_tagger( sent,'pos', True)
                results = []
                for keyword in keywords:
                    keyword = list(keyword)
                    keyword[0] = keyword[0].upper() #대문자
                    results.append(tuple(keyword))
                    for ptr in re.finditer(keyword[0], sent):
                        unit = list(filter(lambda x:
                                        x[2] == ptr.start()-1 and x[1].startswith("S") == True or
                                        x[2] == ptr.end() and x[1].startswith("S") == True, units
                                ))
                        if len(unit) == 2:
                            unit = list(filter(lambda x: x[2] >= ptr.start() and x[2] < ptr.end(), units))
                            if len(unit) == 0: continue
                            while True:
                                if unit[-1][1].startswith("N") == True or len(unit) == 1:
                                    keyword[0] = ''.join(list(list(zip(*unit))[0]))
                                    break
                                else:
                                    del unit[-1]
                            results[-1] = tuple(keyword)
                            cnt = list(list(zip(*results))[0]).count(keyword[0]) #중복 단어 count 후, 제거
                            if cnt > 1: del results[-1]
                            if len(keyword[0]) < 2 : del results[-1] # 1글자 이하 삭제

                            break
            else:
                results = keywords

            keywords_list = []
            for keyword in results:
                keywords_list.append(keyword[0])

            return keywords_list
