from huggingface_hub import InferenceClient

class LLMEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key      
        self.client = InferenceClient(
            model="meta-llama/Llama-3.2-3B-Instruct",
            token=self.api_key
        )
    
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        try:
            # Format prompt for Llama Instruct
            formatted_prompt = f"""<s>[INST] {prompt} [/INST]"""
            
            response = self.client.text_generation(
                formatted_prompt,
                max_new_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response"