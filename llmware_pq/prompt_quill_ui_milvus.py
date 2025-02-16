import gradio as gr
import model_list
import os

from llmware.gguf_configs import GGUFConfigs
GGUFConfigs().set_config("n_gpu_layers", 50)

import torch
test = torch.cuda.is_available()

# you could set this in your env as ENV Variables, to be able to just run we do it like this
os.environ['COLLECTION_DB_URI'] = 'mongodb://192.168.0.127:27017/'
os.environ['MILVUS_HOST'] = '192.168.0.127'
os.environ['MILVUS_PORT'] = '19530'
import llm_interface_milvus

interface = llm_interface_milvus.LLM_INTERFACE()
def set_model(model, temperature, max_tokens, top_k, instruct):
	return interface.change_model(model, temperature, max_tokens, top_k, instruct)
def set_prompt(prompt_text):
	return interface.set_prompt(prompt_text)



css = """
.gr-image {
  min-width: 60px !important;
  max-width: 60px !important;
  min-heigth: 65px !important;
  max-heigth: 65px !important;  
  
}
.app-title {
  font-size: 50px;
}
"""

with gr.Blocks(css=css) as pq_ui:

	with gr.Tab("Chat"):

		with gr.Row():
			# Image element (adjust width as needed)
			gr.Image("logo/pq_v_small.jpg",width="20vw",show_label=False,show_download_button=False,container=False, elem_classes="gr-image",)

			# Title element (adjust font size and styling with CSS if needed)
			gr.Markdown("**Prompt Quill**", elem_classes="app-title")  # Add unique ID for potential CSS styling

		gr.ChatInterface(
			interface.run_llm_response,
			chatbot=gr.Chatbot(height=500,render=False,elem_id="chatbot"),
			textbox=gr.Textbox(placeholder="Enter your prompt to work with",
							   container=False,
							   scale=7,
							   render=False, # render is false as we are in a blocks environment
							   ),
			theme="soft",
			examples=['A fishermans lake','night at cyberpunk city','living in a steampunk world'],
			cache_examples=True,
			retry_btn="🔄  Retry",
			undo_btn="↩️ Undo",
			clear_btn="Clear"
		)

	with gr.Tab("Character"):
		gr.Interface(
			set_prompt,
			[	gr.TextArea(interface.prompt_template,lines = 20),],
			outputs=None,
			allow_flagging='never',
			flagging_options=None,


		)

	with gr.Tab("Model Settings"):
		gr.Interface(
			set_model,
			[

				gr.Dropdown(
					model_list.model_list.keys(),value=list(model_list.model_list.keys())[0], label="LLM Model", info="Will add more LLMs later!"
				),
				gr.Slider(0, 1, step= 0.1, value=0.0, label="Temperature", info="Choose between 0 and 1"),
				gr.Slider(0, 1024, step= 1, value=200, label="max output Tokens", info="Choose between 1 and 1024"),
				gr.Slider(0, 50, step= 1, value=5, label="how many entrys to be fetched from the vector store", info="Choose between 1 and 50 be careful not to overload the context window of the LLM"),
				gr.Checkbox(label='Instruct Model')

			]
			,outputs="text",
			allow_flagging='never',
			flagging_options=None
		)

if __name__ == "__main__":
	pq_ui.launch() #share=True