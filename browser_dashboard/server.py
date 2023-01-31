
from fastapi import WebSocket
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from browser_dashboard.model import Model
import inspect
import numpy as np

class CustomAPI(FastAPI):
    model = None

    def init_iter(self):
        if self.model:
            self.model.stop()
        self.model = self.model_obj(seed=self.seed, gfx=True, **self.model_params)
        # assert inspect.isgeneratorfunction(self.model.__iter__), "Model.__iter__() needs to return generator function (must contain a yield somewhere)."
        iterator = iter(self.model)
        return iterator

    def __init__(self, model_obj: Model, vis_modules, model_params=None, update_gfx_every_x_steps=1, fast_forward_update=100):
        self.seed = 0
        self.fast_forward_update = fast_forward_update
        self.update_gfx_every_x_steps = update_gfx_every_x_steps
        self.model_obj = model_obj
        self.model_params = model_params if model_params is not None else {}
        self.local_includes = []
        self.js_code = []
        self.vis_modules = vis_modules
        self.package_includes = ['runcontrol.js']
        for i in self.vis_modules:
            self.package_includes.extend(i.package_includes)
            self.local_includes.extend(i.local_includes)
            self.js_code.append(i.js_code)
        super().__init__()
        self.template_path = os.path.dirname(__file__) + "/templates/"
        self.mount("/static", StaticFiles(directory=self.template_path), name="static")
        self.templates = Jinja2Templates(directory=self.template_path)
        self.iterator = self.init_iter()

        @self.get("/local/{file_name:path}")
        async def read_load(file_name: str):
            return FileResponse(file_name)

        @self.get("/", response_class=HTMLResponse)
        async def read_item(request: Request):
            return self.templates.TemplateResponse("index.html",
                                                   {"request": request,
                                                    'package_includes': self.package_includes,
                                                    'local_includes': self.local_includes,
                                                    'js_code': self.js_code})

        @self.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            viz_messages = self.viz_state_message()
            await websocket.send_json(viz_messages)

            while True:
                msg = await websocket.receive_text()
                msg = json.loads(msg)

                if msg["type"] == 'get_step':

                    self.model.gfx = False
                    [next(self.iterator) for _ in range(self.update_gfx_every_x_steps-1)]
                    self.model.gfx = True
                    next(self.iterator)

                    viz_messages = self.viz_state_message()
                    self.after_step(self.model)
                    await websocket.send_json(viz_messages)

                elif msg["type"] == 'reset':
                    [i.reset() for i in self.vis_modules]
                    self.seed += 1
                    self.iterator = self.init_iter()
                    await websocket.send_json(self.viz_state_message())

                elif msg["type"] == "close_socket":
                    print("Not Implemented Yet")
                    await websocket.send_json(self.viz_state_message())

                elif msg["type"] == "keyboard_command":
                    result = self.keyboard_command(websocket, msg["command"])
                    if inspect.isawaitable(result):
                        await result
                elif msg["type"] == "switch_fast":
                    self.update_gfx_every_x_steps = self.fast_forward_update if self.update_gfx_every_x_steps == 1 else 1
                else:
                    result = self.other_message(websocket, msg)
                    if inspect.isawaitable(result):
                        await result

    def keyboard_command(self, websocket, key):
        return None

    def other_message(self, websocket, msg):
        return None

    def after_step(self, model):
        return None

    def viz_state_message(self, step=True, only_update=None):
        viz_state = []
        ## Update all viz modules
        for vis_mod in self.vis_modules:
            if only_update is None or np.any([isinstance(vis_mod, i) for i in only_update]):
                viz_state.append(vis_mod.render(self.model))
            else:
                viz_state.append([])
        return {'type': f'viz_state_{"step" if step else "nostep"}', 'data': viz_state}
