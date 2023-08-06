from typing import Tuple

from transformers import AutoModel, AutoTokenizer
import torch
from torch import nn, Tensor


class BinaryYAFAL(nn.Module):
    def __init__(self, label_encoding_size: int,
                 pretrained_model_name: str = "distilbert-base-uncased",
                 mlp_layer_sizes: Tuple[int] = (150, ),
                 llm_output_shape: int = 768
                 ):
        super(BinaryYAFAL, self).__init__()
        self.__model_name = pretrained_model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.__model_name)
        self.bert = AutoModel.from_pretrained(self.__model_name)
        self.linear1 = nn.Linear(llm_output_shape+label_encoding_size, mlp_layer_sizes[0])
        self.__llm_size = llm_output_shape
        self.linear_layers = [
        ]
        for i in range(1, len(mlp_layer_sizes)):
            self.linear_layers.append(
                nn.Linear(mlp_layer_sizes[i-1], mlp_layer_sizes[i])
            )

        self.final_layer = nn.Linear(mlp_layer_sizes[-1], 1)

    def _get_classifier_token_embedding(self, sequence_output):
        return sequence_output[:, 0, :].view(-1, self.__llm_size)

    def forward(self, text, label_encoding: Tensor):
        tokenization_output = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=50,
                                             add_special_tokens=True)

        sequence_output = self.bert(**tokenization_output)

        classify_tensor = self._get_classifier_token_embedding(sequence_output.last_hidden_state)

        # Sequence_output has the following shape: (batch_size, sequence_length, 768)
        # Join the output with the label encoding representation
        concatenate_layer = torch.cat((classify_tensor, label_encoding), 1)
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
