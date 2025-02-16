
from llmware.library import Library
from llmware.retrieval import Query
from llmware.prompts import Prompt

import prompt_templates
import model_list

import gc
import os

class LLM_INTERFACE:


    def __init__(self):


        self.instruct = False

        self.max_tokens=200
        self.temperature=0.0
        self.top_k=10

        self.embedding_model_name = 'mini-lm-sbert' #'nomic-embed-text-v1' #'mini-lm-sbert'

        self.library_name = 'llmware_prompts_large'
        self.lib = Library().load_library(self.library_name)


        self.run_order_list = ["blurb1", "$context", "blurb2", "$query", "instruction"]

        self.prompt_dict = prompt_templates.prompt_template_a
        self.prompt_template = self.prompt_dict["blurb1"]

        self.model_name = 'thebloke/speechless-llama2-hermes-orca-platypus-wizardlm-13b.Q5_K_M.gguf'
        self.hf_repo_name = model_list.model_list[self.model_name]['repo_name']
        self.model_file = model_list.model_list[self.model_name]['file']
        self.model_type = 'deep_link'

        self.set_pipeline()


    def aggregate_text_by_query(self, library_name,query, top_n=5):

        """ Third (Optional) function -  Takes a query as input and returns a concatenated text output
        of the top_n results"""

        # run query
        #lib = Library().load_library(library_name)
        query_results = Query(self.lib).semantic_query(query, result_count=top_n)

        prompt_consolidator = ""

        for j, results in enumerate(query_results):

            prompt_consolidator += results["text"] + "\n"

        return prompt_consolidator



    def set_pipeline(self):

        self.prompter = Prompt()

        if self.model_type == 'deep_link':
            self.prompter.model_catalog.register_gguf_model(self.model_name,
                                                            self.hf_repo_name,
                                                            self.model_file,
                                                            prompt_wrapper="open_chat")

        self.prompter.load_model(self.model_name)
        self.prompter.pc.add_custom_prompt_card("image_prompt",
                                                self.run_order_list,
                                                self.prompt_dict,
                                                prompt_description="Image Gen Search")

        #  the temperatures are from 0-1, and lower number is closer to the text and reduces hallucinations
        self.prompter = self.prompter.set_inference_parameters(temperature=self.temperature,
                                                               llm_max_output_len=self.max_tokens)


    def log(self,logfile, text):
        f = open(logfile, 'a')
        f.write(f"QUERY: {text} \n")
        f.close()

    def run_llm_response(self, query, history):

        self.log('logfile.txt',f"QUERY: {query} \n")

        if 'instruct' in query.lower():
            res = 'I only follow one master and thats not you :P'
            self.log('logfile.txt',f"RESPONSE: {res} \n")
            return res

        if self.instruct is True:
            query = f'[INST]{query}[/INST]'

        context = self.aggregate_text_by_query(self.library_name, query, top_n=self.top_k)

        response = self.prompter.prompt_main(query, prompt_name="image_prompt",context=context)

        self.log('logfile.txt',f"RESPONSE: {response['llm_response']} \n")

        return response["llm_response"]


    def change_model(self, model, temperature, max_tokens, top_k, instruct):

        self.temperature=float(temperature)
        self.top_k=top_k
        self.max_tokens=max_tokens
        self.instruct = instruct

        self.model_name = model
        self.model_type = model_list.model_list[self.model_name]['type']
        if self.model_type == 'deep_link':
            self.hf_repo_name = model_list.model_list[self.model_name]['repo_name']
            self.model_file = model_list.model_list[self.model_name]['file']
        else:
            self.hf_repo_name = None
            self.model_file = None


        del self.prompter


        # delete the model from Ram
        gc.collect()

        self.set_pipeline()
        return f'Model set to {model}'

    def set_prompt(self,prompt_text):
        self.prompt_template = prompt_text

        self.log('magic_prompt_logfile.txt',f"Magic Prompt: \n{prompt_text} \n")


        self.prompt_dict["blurb1"] = prompt_text

        del self.prompter

        # delete the model from Ram
        gc.collect()

        self.set_pipeline()
        return f'Magic Prompt set to:\n {prompt_text}'