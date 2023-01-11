# Copyright 2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import autoai_libs.transformers.text_transformers

import lale.docstrings
import lale.operators


# This is currently needed just to hide get_params so that lale does not call clone
# when doing a defensive copy
class _TextTransformerImpl:
    def __init__(self, **hyperparams):
        if hyperparams.get("column_headers_list", None) is None:
            hyperparams["column_headers_list"] = []
        if hyperparams.get("columns_to_be_deleted", None) is None:
            hyperparams["columns_to_be_deleted"] = []

        self._wrapped_model = (
            autoai_libs.transformers.text_transformers.TextTransformer(**hyperparams)
        )

    def fit(self, X, y=None):
        self._wrapped_model.fit(X, y)
        return self

    def transform(self, X):
        return self._wrapped_model.transform(X)


_hyperparams_schema = {
    "allOf": [
        {
            "description": """TextTransformer is a transformer that converts text columns to numeric features.""",
            "type": "object",
            "additionalProperties": False,
            "required": [
                "text_processing_options",
                "column_headers_list",
                "drop_columns",
                "min_num_words",
                "columns_to_be_deleted",
                "text_columns",
                "activate_flag",
            ],
            "relevantToOptimizer": [],
            "properties": {
                "text_processing_options": {
                    "description": """A map of the transformers to be applied and the hyper parameters of the transformers.
{TextTransformersList.word2vec:{'output_dim':vocab_size}}""",
                    "type": "object",
                    "default": {},
                },
                "column_headers_list": {
                    "description": """The list of columns generated by autoai's processing.
The column headers of the generated features will be appended to this and returned.""",
                    "anyOf": [
                        {"type": "array", "items": {"type": "string"}},
                        {"type": "array", "items": {"type": "integer"}},
                        {"enum": [None]},
                    ],
                    "default": None,
                },
                "drop_columns": {
                    "description": "If the original text columns need to be dropped.",
                    "type": "boolean",
                    "default": False,
                },
                "min_num_words": {
                    "description": "The minimum numbers of words a column must have in order to be considered as a text column.",
                    "type": "integer",
                    "default": 3,
                },
                "columns_to_be_deleted": {
                    "description": "List of columns to be deleted.",
                    "anyOf": [
                        {"type": "array", "items": {"type": "string"}},
                        {"type": "array", "items": {"type": "integer"}},
                        {"enum": [None]},
                    ],
                    "default": None,
                },
                "text_columns": {
                    "description": "If text columns are sent, then text detection is not done again.",
                    "anyOf": [
                        {"type": "array", "items": {"type": "string"}},
                        {"type": "array", "items": {"type": "integer"}},
                        {"enum": [None]},
                    ],
                    "default": None,
                },
                "activate_flag": {
                    "description": "If False, the features are not generated.",
                    "type": "boolean",
                    "default": True,
                },
            },
        }
    ]
}

_input_fit_schema = {
    "type": "object",
    "required": ["X"],
    "additionalProperties": False,
    "properties": {
        "X": {  # Handles 1-D arrays as well
            "anyOf": [
                {"type": "array", "items": {"laleType": "Any"}},
                {
                    "type": "array",
                    "items": {"type": "array", "items": {"laleType": "Any"}},
                },
            ]
        },
        "y": {"laleType": "Any"},
    },
}

_input_transform_schema = {
    "type": "object",
    "required": ["X"],
    "additionalProperties": False,
    "properties": {
        "X": {  # Handles 1-D arrays as well
            "anyOf": [
                {"type": "array", "items": {"laleType": "Any"}},
                {
                    "type": "array",
                    "items": {"type": "array", "items": {"laleType": "Any"}},
                },
            ]
        }
    },
}

_output_transform_schema = {
    "description": "Features; the outer array is over samples.",
    "anyOf": [
        {"type": "array", "items": {"laleType": "Any"}},
        {"type": "array", "items": {"type": "array", "items": {"laleType": "Any"}}},
    ],
}

_combined_schemas = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": """Operator from `autoai_libs`_. Converts text columns to numeric features using a combination of word2vec and SVD.
.. _`autoai_libs`: https://pypi.org/project/autoai-libs""",
    "documentation_url": "https://lale.readthedocs.io/en/latest/modules/lale.lib.autoai_libs.word2vec_transformer.html",
    "import_from": "autoai_libs.transformers.text_transformers",
    "type": "object",
    "tags": {"pre": [], "op": ["transformer"], "post": []},
    "properties": {
        "hyperparams": _hyperparams_schema,
        "input_fit": _input_fit_schema,
        "input_transform": _input_transform_schema,
        "output_transform": _output_transform_schema,
    },
}

TextTransformer = lale.operators.make_operator(_TextTransformerImpl, _combined_schemas)

lale.docstrings.set_docstrings(TextTransformer)
