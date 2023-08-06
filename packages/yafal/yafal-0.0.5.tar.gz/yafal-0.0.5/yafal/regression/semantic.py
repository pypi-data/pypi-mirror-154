from typing import Tuple, List

from transformers import AutoModel, AutoTokenizer
import torch
from torch import nn


class SemanticYAFAL(nn.Module):
    def __init__(self,
                 pretrained_model_name: str = "distilbert-base-uncased",
                 max_sequence_size: int = 128,
                 max_label_encoding_size: int = 50,
                 mlp_layer_sizes: Tuple[int] = (150,),
                 llm_output_size: int = 768,
                 label_encoding_size: int = 768
                 ):
        super(SemanticYAFAL, self).__init__()
        self.__model_name = pretrained_model_name
        self.__max_sequence_size = max_sequence_size
        self.__max_label_seq_size = max_label_encoding_size
        # Input encoder
        self.tokenizer = AutoTokenizer.from_pretrained(self.__model_name)
        self.bert = AutoModel.from_pretrained(self.__model_name)
        # Label encoder
        self.label_tokenizer = AutoTokenizer.from_pretrained(self.__model_name)
        self.label_bert = AutoModel.from_pretrained(self.__model_name)

        # Define the rest of the layers
        self.linear1 = nn.Linear(llm_output_size + label_encoding_size, mlp_layer_sizes[0])
        self.linear_layers = [
        ]
        for i in range(1, len(mlp_layer_sizes)):
            self.linear_layers.append(
                nn.Linear(mlp_layer_sizes[i - 1], mlp_layer_sizes[i])
            )

        self.final_layer = nn.Linear(mlp_layer_sizes[-1], 1)

    @staticmethod
    def _get_classifier_token_embedding(sequence_output):
        return sequence_output[:, 0, :].view(-1, 768)

    def forward(self, text: List[str], label_text: List[str]):
        tokenization_output = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True,
                                             max_length=self.__max_sequence_size,
                                             add_special_tokens=True)

        sequence_output = self.bert(**tokenization_output)

        classify_tensor = self._get_classifier_token_embedding(sequence_output.last_hidden_state)

        # Encode the label
        label_tokenization = self.label_tokenizer(label_text, return_tensors='pt', padding=True, truncation=True,
                                                  max_length=self.__max_label_seq_size,
                                                  add_special_tokens=True)
        label_output = self.label_bert(**label_tokenization)

        label_encoding_tensor = self._get_classifier_token_embedding(label_output.last_hidden_state)

        # Join the output with the label encoding representation
        concatenate_layer = torch.cat((classify_tensor, label_encoding_tensor), 1)

        linear_output = self.linear1(concatenate_layer)
        for linear_layer in self.linear_layers:
            tanh_result = nn.Tanh()
            tanh_output = tanh_result(linear_output)
            linear_output = linear_layer(tanh_output)
        tanh_result = nn.Tanh()
        tanh_output = tanh_result(linear_output)
        linear2_output = self.final_layer(tanh_output)
        sigmoid_result = nn.Sigmoid()
        return sigmoid_result(linear2_output)
