from typing import Optional

from toolva.tasks import (
                   # KeywordFactory,
                   # KnlyMD,
                   SentimentsFactory,
                   # NerFactory,
                   EmbedFactory
                   )

SUPPORTED_TASKS = {
    # "keyword" : KeywordFactory,
    # "konlpy" : KnlyMD,
    "sentiments" : SentimentsFactory,
    # "ner" : NerFactory,
    "embeder" : EmbedFactory}


class Toolva:

    def __new__(cls, task: str, model: Optional[str]=None , **kwargs) :

        if task not in SUPPORTED_TASKS:
            raise KeyError("Unknown task {}, available tasks are {}".format(
                task,
                list(SUPPORTED_TASKS.keys()),
            ))

        # if model is None:
        #     raise KeyError("plz prepare your model")
        #     ))

        # Instantiate task-specific pipeline module, if possible
        if task == 'ner':
            pred_config = kwargs.get("pred_config", 0)
            if pred_config == 0:
                raise KeyError("plz put your own pred_config")
            else:
                task_module = SUPPORTED_TASKS[task](pred_config)

        else:
            task_module = SUPPORTED_TASKS[task](model)

        return task_module

        # Get device information from torch API
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

