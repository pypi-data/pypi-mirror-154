from typing import Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline


class SentimentsFactory:
    """
    Classification based sentiment analysis using Review Corpus

    Examples:
        >>> sa = package(task="sentiments", model= model_path )
        >>> sa("배송이 버트 학습시키는 것 만큼 느리네요")
        'N'
        >>> sa("배송이 경량화되었는지 빠르네요")
        'P'
        >>> sa("이걸 산 내가 레전드", show_probs=True)
        [{'label': 'LABEL_1', 'score': 0.9877371788024902}]
    """

    def __init__(self, model: Optional[str]):

        if model is None:
            model_path = self.get_available_models()["klue_base"]
        else:
            model_path = model

        classifier = AutoModelForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        nlp_sentence_classif = pipeline('sentiment-analysis', model=classifier, tokenizer=tokenizer, device=0)
        self.nlp_sentence_classif = nlp_sentence_classif

    @staticmethod
    def get_available_models():
        return {
            "klue_base":
                'samba/samba-sentiments-fine-tuned'
        }

    def __call__(self, sent: str, **kwargs): # package의 인스턴스를 인스터스화 했을때 호출

        return self.predict(sent, **kwargs)

    def predict(self, sent: str, **kwargs):
        show_probs = kwargs.get("show_probs", False)

        res = self.nlp_sentence_classif(sent)

        # Label_1 = 긍정 / Label_0 = 부정
        if show_probs:
            return res  # [{'label': 'LABEL_1', 'score': 0.9877371788024902}]

        else:
            if res[0]['label'] == 'LABEL_1':
                label = 'P'
            else:
                label = 'N'

            return label  # "P" or "N"


