import numpy as np
import tensorflow as tf

class Classifier(object):
    def __init__(
        self,
        model_path = 'models/classifier.tflite',
        num_threads=1,
    ):
        
        self.interpreter = tf.lite.Interpreter(model_path = model_path,
                                               num_threads = num_threads)
        
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        self.score_th = score_th
        self.invalid_value = invalid_value
        
    def __call__(
      self,
      landmark_list,
    ):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_Tensor(
            input_details_tensor_index,
            np.array([landmark_list],dtype=np.float32)
        )