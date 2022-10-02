from fastapi import WebSocket
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from gym_browser_dashboard.model import Model
import inspect
class CustomAPI(FastAPI):
    model = None

    def init_iter(self):
        if self.model:
            self.model.stop()
        self.model = self.model_obj(**self.model_params)
        assert inspect.isgeneratorfunction(self.model.step), "Model.step() needs to be a generator function (must contain a yield somewhere)."
        iterator = self.model.step()
        return iterator

    def __init__(self, model_obj: Model, vis_modules, model_params):
        self.model_obj = model_obj
        self.model_params = model_params
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
            while True:
                msg = await websocket.receive_text()
                msg = json.loads(msg)

                if msg["type"] == 'get_step':
                    next(self.iterator)
                    await websocket.send_json(self.viz_state_message)

                elif msg["type"] == 'reset':
                    self.iterator = self.init_iter()
                    await websocket.send_json(self.viz_state_message)

                elif msg["type"] == "close_socket":
                    print("Not Implemented Yet")
                    await websocket.send_json(self.viz_state_message)


    @property
    def viz_state_message(self):
        viz_state = []
        ## Update all viz modules
        for vis_mod in self.vis_modules:
            viz_state.append(vis_mod.render(self.model))
        return {'type': 'viz_state', 'data': viz_state}


