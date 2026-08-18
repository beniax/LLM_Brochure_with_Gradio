import gradio as gr
from method_utils import create_brochure


model=""
 
def stream_model(company_name,url,model):
    if model=='GPT':
        result = create_brochure(company_name,url,model)
    elif model=='GEMINI':
        result = create_brochure(company_name,url,model)
    elif model=='Ollama':
        result = create_brochure(company_name,url,model)
    else:
        raise ValueError("No model found")
    
        
    yield from result
    
    
message_input_compny_name = gr.Textbox(label="Your message:", info="Enter Company Name")
message_input_url = gr.Textbox(label="Your message:", info="Enter an URL for brochurement")
modular_selector = gr.Dropdown(['GPT','GEMINI','Ollama'],label='Select model',value="gpt-4.1-mini")
message_output = gr.Textbox(label="Response:")

gr.Interface(
    fn=stream_model,
    title='LLMS',
    inputs=[message_input_compny_name,message_input_url,modular_selector],
    outputs=[message_output],
    examples=[['Hugging Face','https://www.huggingface.com/','GPT'],['AI Engineer by edward donner','https://edwarddonner.com/','GEMINI']],
    flagging_mode='never',
    theme=gr.themes.Default(
        primary_hue="green",
        neutral_hue="slate"
    )   
).launch(inbrowser=True)
    