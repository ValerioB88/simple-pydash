import time
from fastapi import WebSocket
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from simple_pydash.model import Model
import inspect
import numpy as np
import sty


class CustomAPI(FastAPI):
    model = None

    def init_iter(self):
        if self.model:
            self.model.stop()
        self.model = self.model_obj(seed=self.seed, gfx=True, **self.model_params)
        iterator = iter(self.model)
        return iterator

    def __init__(
        self,
        model_obj: Model,
        dash_comps,
        model_params=None,
        seed=None,
        num_widget_columns=None,
        fast_forward_update=100,
        wide_page=None,
    ):
        self.seed = int(time.time()) % (2**32 - 1) if seed is None else seed
        self.iters_per_gfx_update = 1
        self.fast_forward_update = fast_forward_update
        self.model_obj = model_obj
        self.model_params = model_params if model_params is not None else {}
        self.local_includes = []
        self.js_code = []
        self.dash_comps = dash_comps
        self.package_includes = ["runcontrol.js"]
        widget_max_cols = max([i.location_col_idx for i in dash_comps]) + 1
        if num_widget_columns is not None and widget_max_cols > num_widget_columns:
            print(
                sty.fg.red
                + f"The number of requested columns {num_widget_columns} is lower than the maximum columns implied by the maximum column index for some widget: {widget_max_cols-1}. We will use {widget_max_cols} columns"
                + sty.rs.fg
            )
        num_widget_columns = 2 if num_widget_columns is None else num_widget_columns
        if num_widget_columns > 6:
            print(
                sty.fg.red + "Having more than 6 columns is not supported" + sty.rs.fg
            )
            num_widget_columns = 6
        self.num_widget_columns = max(widget_max_cols, num_widget_columns)

        self.wide_page = wide_page
        if self.wide_page is None:
            self.wide_page = True if self.num_widget_columns > 2 else False

        for i in self.dash_comps:
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
            return self.templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "package_includes": self.package_includes,
                    "local_includes": self.local_includes,
                    "js_code": self.js_code,
                    "column_ids": [str(i) for i in range(self.num_widget_columns)],
                    "num_columns": self.num_widget_columns,
                    "wide_page": self.wide_page,
                },
            )

        @self.websocket_route("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            while True:
                msg = json.loads(await websocket.receive_text())
                if msg["type"] == "get_step":
                    all_viz_messages = []
                    for _ in range(self.iters_per_gfx_update):
                        # self.model.gfx = False
                        # [next(self.iterator) for _ in range(self.update_gfx_every_x_steps - 1)]
                        # self.model.gfx = True
                        next(self.iterator)

                        viz_messages = self.get_one_iter_viz_state_msg()
                        all_viz_messages.append(viz_messages)
                        self.after_step(self.model)

                    await websocket.send_json(
                        {
                            "type": "render_data_multi_iter",
                            "iterations": all_viz_messages,
                        }
                    )
                elif msg["type"] == "change_server_params":
                    setattr(self, msg["param_name"], int(msg["value"]))

                # msg = await websocket.receive_text()
                # msg = json.loads(msg)

                elif msg["type"] == "reset":
                    [i.reset() for i in self.dash_comps]
                    self.seed += 1
                    self.iterator = self.init_iter()
                    await websocket.send_json(
                        {
                            "type": "render_data_multi_iter",
                            "iterations": [self.get_one_iter_viz_state_msg()],
                        }
                    )

                elif msg["type"] == "close_socket":
                    print("Not Implemented Yet")
                    await websocket.send_json(
                        {
                            "type": "render_data_multi_iter",
                            "iterations": [self.get_one_iter_viz_state_msg()],
                        }
                    )

                elif msg["type"] == "keyboard_command":
                    result = self.keyboard_command(websocket, msg["command"])
                    if inspect.isawaitable(result):
                        await result
                # elif msg["type"] == "switch_fast":
                #     self.update_gfx_every_x_steps = (
                #         self.fast_forward_update
                #         if self.update_gfx_every_x_steps == 1
                #         else 1
                #     )
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

    def get_one_iter_viz_state_msg(self, only_update=None):
        viz_state = []
        ## Update all viz modules
        for vis_mod in self.dash_comps:
            if only_update is None or np.any(
                [isinstance(vis_mod, i) for i in only_update]
            ):
                viz_state.append(vis_mod.render(self.model))
            else:
                viz_state.append([])
        return {"data": viz_state}
