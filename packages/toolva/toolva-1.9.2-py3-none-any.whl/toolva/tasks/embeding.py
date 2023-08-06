from typing import Optional
from sentence_transformers import SentenceTransformer

class EmbedFactory:
    """
        Classification based sentiment analysis using Review Corpus

        Examples:
            >>> embed = package(task="embeder", model= model_path )
            >>> embed("배송이 버트 학습시키는 것 만큼 느리네요", mode ='embedding')
            [0.61495 0.54558 -0.80371 0.26671 -0.95319 -0.08139 -0.65604 0.18993 -0.56726 0.13981 -0.04617 0.40250 0.74457 0.40800]
            >>> embed("배송이 버트 학습시키는 것 만큼 느리네요")
            [0.61495 0.54558 -0.80371 0.26671 -0.95319 -0.08139 -0.65604 0.18993 -0.56726 0.13981 -0.04617 0.40250 0.74457 0.40800]
        """
    def __init__(self, model: Optional[str], **kwargs):

        if model is None:
            model_path = self.get_available_models()["klue_base"]
        else:
            model_path = model

        model = SentenceTransformer(model_path)
        self.model = model

    @staticmethod
    def get_available_models():
        return {
            "klue_base":
                'samba/samba-large-bert-fine-tuned'

        }

    def __call__(self, corpus: str, **kwargs):
        # print("Factory에 __call__ 호출")
        return self.predict(corpus, **kwargs)

    def predict(self, corpus: str, **kwargs):

        mode = kwargs.get("mode", 'embedding')  # defalt topn = 10개

        if mode == 'embedding':
            result = self.model.encode(corpus)

            return result
