from openai import OpenAI
import tiktoken

# class for openai manager that handles the init, and custom functions
class AiManager:
    # init function
    def __init__(self):
        self.client = OpenAI()
        self.model_options = self.client.models.list()
        self.model = None
        
    # function to get the model options
    def get_model_options(self):
        print(self.model_options)
        return self.model_options
    
    # function to set the model
    def set_model(self, model):
        self.model = model  
    
    
    
    
    
    
     