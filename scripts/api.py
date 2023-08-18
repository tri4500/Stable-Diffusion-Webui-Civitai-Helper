import modules.scripts as scripts
import gradio as gr
from fastapi import FastAPI, Body

import modules
from modules import script_callbacks
from modules import shared
from scripts.ch_lib import model
from scripts.ch_lib import js_action_civitai
from scripts.ch_lib import model_action_civitai
from scripts.ch_lib import setting
from scripts.ch_lib import civitai
from scripts.ch_lib import util


def civitaiAPI(_: gr.Blocks, app: FastAPI):
    def init():
      root_path = os.getcwd()
      extension_path = scripts.basedir()
      model.get_custom_model_folder()
      setting.load()
      if setting.data["general"]["proxy"]:
        util.printD("Set Proxy: "+setting.data["general"]["proxy"])
        util.proxies = {
            "http": setting.data["general"]["proxy"],
            "https": setting.data["general"]["proxy"],
        }

    @app.post('/civitai/v1/scan-model')
    def link_status(scan_model_types: list = Body(["ti", "hyper", "ckp", "lora"],title="List of model types"),
              max_size_preview: bool= Body(True,title="Download Max Size Preview"),
              skip_nsfw_preview: bool =Body(False,title="Skip NSFW Preview Images")):
        result = model_action_civitai.scan_model(scan_model_types, max_size_preview, skip_nsfw_preview)
        return { "result": result }
    
    @app.get('/civitai/v1/info-by-url')
    def link_status(url: str = None):
        r = model_action_civitai.get_model_info_by_url(url)
        model_info = {}
        model_name = ""
        model_type = ""
        subfolders = []
        version_strs = []
        if r:
            model_info, model_name, model_type, subfolders, version_strs = r
        return {
           "model_info": model_info,
           "model_name": model_name,
           "model_type": model_type,
           "subfolders": subfolders,
           "versions": version_strs
        }

script_callbacks.on_app_started(civitaiAPI)