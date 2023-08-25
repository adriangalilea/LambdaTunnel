from gradio_client import Client

class GradioAPIWrapper:
    def __init__(self, base_url="http://127.0.0.1:7860/"):
        self.client = Client(base_url)

    def predict_fn0(self, random):
        return self.client.predict(random, fn_index=0)

    def predict_fn1(self):
        return self.client.predict(fn_index=1)

    def predict_fn2(self, advanced):
        return self.client.predict(advanced, fn_index=2)

    def predict_fn3(self, random, seed):
        return self.client.predict(random, seed, fn_index=3)

    def predict_fn4(self, parameter_8, negative_prompt, parameter_23, performance, aspect_ratios, image_number, seed, sampling_sharpness, sdxl_base_model, sdxl_refiner, sdxl_lora1, weight1, sdxl_lora2, weight2, sdxl_lora3, weight3, sdxl_lora4, weight4, sdxl_lora5, weight5):
        return self.client.predict(parameter_8, negative_prompt, parameter_23, performance, aspect_ratios, image_number, seed, sampling_sharpness, sdxl_base_model, sdxl_refiner, sdxl_lora1, weight1, sdxl_lora2, weight2, sdxl_lora3, weight3, sdxl_lora4, weight4, sdxl_lora5, weight5, fn_index=4)
