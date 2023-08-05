#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import List, Optional
from bigdl.nano.deps.neural_compressor.inc_api import quantize as inc_quantzie
import tensorflow as tf
from tensorflow.keras.metrics import Metric
from bigdl.nano.utils.log4Error import invalidInputError


def quantize(self,
             calib_dataset: tf.data.Dataset = None,
             metric: Optional[Metric] = None,
             backend='inc',
             conf: Optional[str] = None,
             approach='static',
             tuning_strategy='bayesian',
             accuracy_criterion: dict = {'relative': 0.99, 'higher_is_better': True},
             timeout=0,
             max_trials=1,
             inputs: List[str] = None,
             outputs: List[str] = None):
    """
    Post-training quantization on a keras model.

    :param calib_dataset:  A tf.data.Dataset object for calibration. Required for
                            static quantization.
    :param val_dataset:    A tf.data.Dataset object for evaluation.
    :param batch:          Batch size of dataloader for both calib_dataset and val_dataset.
    :param metric:         A Metric object for evaluation.
    :param backend:        Only support 'inc' for now. Default: 'inc'.
    :param conf:           A path to conf yaml file for quantization.
                            Default: None, using default config.
    :param approach:       'static' or 'dynamic'.
                            'static': post_training_static_quant,
                            'dynamic': post_training_dynamic_quant.
                            Default: 'static'.
    :param tuning_strategy:    'bayesian', 'basic', 'mse', 'sigopt'. Default: 'bayesian'.
    :param accuracy_criterion: Tolerable accuracy drop.
                                accuracy_criterion = {'relative': 0.1, 'higher_is_better': True}
                                allows relative accuracy loss: 1%. accuracy_criterion =
                                {'absolute': 0.99, 'higher_is_better':False} means accuracy
                                must be smaller than 0.99.
    :param timeout:    Tuning timeout (seconds). Default: 0,  which means early stop.
                        Combine with max_trials field to decide when to exit.
    :param max_trials: Max tune times. Default: 1.
                        Combine with timeout field to decide when to exit.
                        "timeout=0, max_trials=1" means it will try quantization only once and
                        return satisfying best model.
    :param inputs:     A list of input names.
                        Default: None, automatically get names from graph.
    :param outputs:    A list of output names.
                        Default: None, automatically get names from graph.
    :return:           A TensorflowBaseModel for INC. If there is no model found, return None.
    """
    if backend == 'inc':
        return inc_quantzie(self, dataloader=calib_dataset, metric=metric,
                            framework='tensorflow',
                            conf=conf,
                            approach=approach,
                            tuning_strategy=tuning_strategy,
                            accuracy_criterion=accuracy_criterion,
                            timeout=timeout,
                            max_trials=max_trials,
                            inputs=inputs,
                            outputs=outputs)
    else:
        invalidInputError(False, "Backend {} is not implemented.".format(backend))
