from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import torch
import os


class NerFactory:

    def __init__(self, pred_config):
        """
            Examples:
                >>> ner = package(task="ner", model= model_path )
                >>> ner("홍길동은 지금 시장에 가려고 광화문에서 버스를 탔습니다.")
                [{'NECode': 'PS', 'NEwords': '홍길동'}, {'NECode': 'LC', 'NEwords': '광화문'}]
            """
        self.pred_config = pred_config

        device = self.get_device()
        self.device = device

        fine_tuned_model_ckpt = self.load_fine_tuned_model()
        self.fine_tuned_model_ckpt = fine_tuned_model_ckpt

        model_args = self.get_model_args()
        self.model_args = model_args

        model = self.load_model()
        self.model = model

        tokenizer = AutoTokenizer.from_pretrained(pred_config.pretrained_model_name, use_fast=True)
        self.tokenizer  = tokenizer

        label_list = self.get_labels()
        self.label_list = label_list


    def get_device(self):
        return "cuda" if torch.cuda.is_available() and not self.pred_config.no_cuda else "cpu"

    def load_fine_tuned_model(self):
        return torch.load(self.pred_config.downstream_model_dir, map_location=self.device)

    def get_model_args(self):
        return self.fine_tuned_model_ckpt['hyper_parameters']

    def load_tokenizer(self):
        return  self.model_args['tokenizer']

    def get_labels(self):
        return  self.model_args['label_list']

    def load_model(self):
        model_dir =  self.model_args['output_dir'] + '/transformers'
        # Check whether model exists
        if not os.path.exists(model_dir):
            raise Exception("Model doesn't exists! Train first!")
        try:
            model = AutoModelForTokenClassification.from_pretrained(
                model_dir)  # Config will be automatically loaded from model_dir
            model.eval().to(self.device)
            # model.eval()
        except:
            raise Exception("Some model files might be missing...")
        return model

    def __call__(self, ner_df, **kwargs): # package의 인스턴스를 인스터스화 했을때 호출
        ner_pre = self.predict(ner_df, **kwargs)#(pred_config, ner_df, model, tokenizer, label_list, model_args, device)

        return self.indexing_es(ner_pre)


#======================model 이후 predict에 필요한 함수=================================================
    def indexing_es(self, result):
        for idx in range(len(result)):  # len(result)
            col_PS = result['PS'][idx]
            col_LC = result['LC'][idx]
            col_OG = result['OG'][idx]

            list_ne = []

            if col_PS is not None:
                for idx_ps, words_ps in enumerate(col_PS):
                    dic_ne = {"NECode": "PS", 'NEwords': words_ps}
                    list_ne.append(dic_ne)
            else:
                pass

            if col_LC is not None:
                for idx_ps, words_ps in enumerate(col_LC):
                    dic_ne = {"NECode": "LC", 'NEwords': words_ps}
                    list_ne.append(dic_ne)
            else:
                pass

            if col_OG is not None:
                for idx_ps, words_ps in enumerate(col_OG):
                    dic_ne = {"NECode": "OG", 'NEwords': words_ps}
                    list_ne.append(dic_ne)
            else:
                pass

            return list_ne

    def read_input_file(self, doc):
        lines = doc.split('\n')
        doc = []
        for line in lines:
            words = line.strip()
            words = line.split()
            doc.append(words)
        return doc


    def convert_input_file_to_tensor_dataset(self, lines,
                                             args,
                                             tokenizer,
                                             cls_token_segment_id=0,
                                             pad_token_segment_id=0,
                                             sequence_a_segment_id=0,
                                             mask_padding_with_zero=True):
        # Setting based on the current model type
        cls_token = tokenizer.cls_token
        sep_token = tokenizer.sep_token
        unk_token = tokenizer.unk_token
        pad_token_id = tokenizer.pad_token_id

        all_input_ids = []
        all_attention_mask = []
        all_token_type_ids = []

        tokens_list = []
        for words in lines:
            tokens = []
            for word in words:
                word_tokens = tokenizer.tokenize(word)
                if not word_tokens:
                    word_tokens = [unk_token]  # For handling the bad-encoded word
                tokens.extend(word_tokens)
            special_tokens_count = 2
            if len(tokens) > args['max_seq_length'] - special_tokens_count:
                tokens = tokens[: (args['max_seq_length'] - special_tokens_count)]

            # Add [SEP] token
            tokens += [sep_token]

            token_type_ids = [sequence_a_segment_id] * len(tokens)

            # Add [CLS] token
            tokens = [cls_token] + tokens
            token_type_ids = [cls_token_segment_id] + token_type_ids
            input_ids = tokenizer.convert_tokens_to_ids(tokens)
            tokens_list.append(tokens)

            # The mask has 1 for real tokens and 0 for padding tokens. Only real tokens are attended to.
            attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

            # Zero-pad up to the sequence length.
            padding_length = args['max_seq_length'] - len(input_ids)
            input_ids = input_ids + ([pad_token_id] * padding_length)
            attention_mask = attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
            token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)

            all_input_ids.append(input_ids)
            all_attention_mask.append(attention_mask)
            all_token_type_ids.append(token_type_ids)

        # Change to Tensor
        all_input_ids = torch.tensor(all_input_ids, dtype=torch.long)
        all_attention_mask = torch.tensor(all_attention_mask, dtype=torch.long)
        all_token_type_ids = torch.tensor(all_token_type_ids, dtype=torch.long)

        dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids)

        return tokens_list, dataset


    def predict(self, df, **kwargs):
        entity_tags = self.pred_config.entity_tags
        stopwords = self.pred_config.stopwords
        corpus = df[self.pred_config.corpus_col].to_list()
        result = defaultdict(list)

        for doc in tqdm(corpus, desc="Predicting", mininterval=1):
            # Convert input file to TensorDataset
            lines = self.read_input_file(doc)
            tokens_list, dataset = self.convert_input_file_to_tensor_dataset(lines, self.model_args, self.tokenizer)
            # word_tokens = [word_token.strip().replace("##", "") for word_token in word_tokens]

            # Predict
            sampler = SequentialSampler(dataset)
            data_loader = DataLoader(dataset, sampler=sampler, batch_size= self.pred_config.batch_size)

            preds = None

            for batch in data_loader:
                batch = tuple(t.to(self.device) for t in batch)
                with torch.no_grad():
                    inputs = {"input_ids": batch[0],
                              "attention_mask": batch[1],
                              "labels": None,
                              "token_type_ids": batch[2]}
                    outputs = self.model(**inputs)
                    logits = outputs[0]

                    if preds is None:
                        preds = logits.detach().cpu().numpy()
                    else:
                        preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)

            try:
                preds = np.argmax(preds, axis=2)
            except:
                for entity_tag in entity_tags:
                    result[entity_tag].append(None)
                continue
            slot_label_map = {i: label for i, label in enumerate(self.label_list)}
            preds_list = [[] for _ in range(preds.shape[0])]

            for i in range(preds.shape[0]):
                for j in range(len(tokens_list[i])):
                    preds_list[i].append(slot_label_map[preds[i][j]])

            dict_of_ner_word = defaultdict(list)
            for line_idx in range(len(tokens_list)):
                tokens = tokens_list[line_idx]
                tokens = [token.strip().replace("##", "") for token in tokens]
                entity_word, entity_tag, prev_entity_tag = "", "", ""
                for token_idx, tag in enumerate(preds_list[line_idx]):
                    if "B-" in tag:
                        entity_tag = tag[-2:]
                        if prev_entity_tag != entity_tag and prev_entity_tag in entity_tags and len(entity_word) > 1:
                            dict_of_ner_word[prev_entity_tag].append(entity_word)
                        if tokens[token_idx] not in stopwords:
                            entity_word = tokens[token_idx]
                        prev_entity_tag = entity_tag
                    elif "I-" + entity_tag in tag:
                        if tokens[token_idx] not in stopwords:
                            entity_word += tokens[token_idx]
                    else:
                        if entity_tag in entity_tags and len(entity_word) > 1:
                            dict_of_ner_word[entity_tag].append(entity_word)
                        entity_word, entity_tag, prev_entity_tag = "", "", ""

            for entity_tag in entity_tags:
                if dict_of_ner_word.get(entity_tag) == None:
                    result[entity_tag].append(None)
                else:
                    result[entity_tag].append(list(set(dict_of_ner_word[entity_tag])))

        for entity_tag in entity_tags:
            df[entity_tag] = result[entity_tag]

        return df


