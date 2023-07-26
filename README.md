
## SimplePyDash
![Demo](demo.gif)

**SimplePyDash** is a versatile, browser-based dashboard designed for real-time data plotting. With a focus on simplicity, it allows Python developers to easily visualize data streams without complex setup or dependencies.

Although originally developed to facilitate real-time plotting of OpenAI Gym environments for observing agent behavior, the versatility of SimplePyDash extends its utility beyond this use case, making it an excellent tool for many other data visualization scenarios.

Under the hood, SimplePyDash leverages the [FastAPI](https://fastapi.tiangolo.com/) web framework and uses [WebSocket](https://en.wikipedia.org/wiki/WebSocket) for bidirectional communication.

### Requirements:
Use the following command to install necessary dependencies:
```
pip install fastapi "uvicorn[standard]"
```
For working with OpenAI Gym environments, install the `gym` library using the command:
```
pip install gym
```
Note: This library is only needed for running the `examples/openai_gym.py` example and is otherwise not mandatory.

### Installation
To install SimplePyDash, you can _either_:

- Install directly from the repository:
```
pip install git+https://github.com/ValerioB88/browser-dashboard.git
```
**OR**
- Clone/fork the repository, and install in editable mode (recommended if you plan to modify the code):
```
pip install -e {path_to_cloned_folder}
```

### Examples 
The best way to get started is to explore the examples provided. `examples/openai_gym.py` demonstrates plotting a gym environment (requires the `gym` library), while `examples/generic.py` is a more general use case.

To run an example, navigate to the repository folder and execute the Python module:
```
cd {path_to_repo_folder}
python -m examples.gym
```
The script will try to use the first available port starting at `8000`. Open your browser and visit `localhost:8000` (or another port if indicated in the console output).

**If you are running the script on a server**, port forwarding will be necessary. Open a new terminal on your local machine and type:
```
ssh -L {portnum}:localhost:{portnum} {username}@{machinename}
```
For example:
```
ssh -L 8000:localhost:8000 val@titan.it
```
Then, open your browser and visit `localhost:8000` to view the dashboard.

## Quick Start 
SimplePyDash organizes your dashboard into columns (2 by default). The `CustomAPI` object takes a `model_obj` and a series of `DashboardComponents`. The user-defined `model_obj` is a simple iterator performing the computations (e.g., running a neural network and returning an action). `DashboardComponents` are widgets that can be displayed in the browser.

SimplePyDash includes several default widgets, including `HeatMap`, `LinePlot`, `StaticImage`, `TextInfo`, and `RenderGymEnv`. The `plot` widgets, such as `HeatMap` and `LinePlot`, are based on the [Plotly](https://plotly.com/python/) graphics library, allowing for easy addition of Plotly graphs to your widget list.

Here's a basic example of a `CustomAPI` object:
```python
server = CustomAPI(
    model_obj=model,
    dash_comps=[
        GeneralTextInfo(location_col_idx=0, use_scroll=False),
        HeatMap(
            get_new_data_fun=lambda m: np.random.randn(10, 10),
            clr_min=-1,
            clr_max=1,
            location_col_idx=1,
        ),
        AppendLinePlot(
            legends=["Cart Pos", "Cart Vel", "Pole Angle", "Pole Angle Vel"],
            get_new_data_fun=lambda m: [[i] for i in m.obs.tolist()],
            location_col_idx=1,
            height=200,
        ),
    model_params={'env': gym.make("CartPole-v1", render_mode="rgb_array")},
)
```
We'll talk about the `model_obj` in a second. For now consider the `dash_comps` (DashComponents). We provide 3 components, and organize them in 3 different columns, as specified by the fact that their `location_col_idx` is 0, 1, and 2. `SimplePyDash` automatically creates a dashboard with 3 columns. If the `location_col_idx` of the `AppendLinePlot` was `=1`, this would automatically create 2 columns, and place the `GeneralTextInfo` widget in the first one, and the `HeatMap` and `AppendLinePlot` in the second column. Notice that the order in which the widgets are placed in a column corresponds to the order they are passed to `dash_comps`. 

Each `DashComponent` will have a default `width` and `height`. However, you can modify one or both of them to make the widget bigger or smaller. This will not resize the whole column. 

### Model
The `Model` must be an infinite iterator that performs computations for the data you want to plot. Here's a general example for a gym environment:

```python
class DummyGymModel(Model):
    action = 0
    def __init__(self, env):
        self.env = env
        self.obs, _ = self.env.reset()

    def __iter__(self):
        while True:
            self.action = np.random.randint(0, 2)
            self.obs, _, termination, _, _ = env.step(self.action)
            if termination:
                self.obs, _ = env.reset()
            yield None

    def stop(self):
        env.reset()
```
(in a real life scenario, this class will also contain a neural network for taking the action).
It should be simple to adapt your own code to this setup. This `DummyGymModel` only has one parameter: `env`, but you can customize this class as you with. The parameters are passed to the `CustomAPI` object as `model_params`. 
### Plotly Components
`HeatMap` and `AppendLinePlot` are PlotLy components: they are Plotly figures which are passed to the web browser. Implementing a new plotting component just a bit more effort than creating a new Plotly plot: each component needs to implement a `render` function which specifies what to do with the figure at each iteration. For `HeatMap` and `AppendLinePlot`, the `render` function calls a user-provided `get_new_data_fun` which takes some data and use them to update the Plotly figure. In this way the `AppendLinePlot` and `HeatMap` are general and can be used for any model.  However, you can create your own `PlotlyComponent` that simple plots some data specific to your own model. This is easy, since `render` has access to the whole model object, so that you can do something like `self.fig.data[0].z = model.agents[0].energy_level`. . 

#### Canvas
The `Canvas` module returns an image for rendering animations in the browser. This could be an OpenAI rendering (using `RenderGymEnv` module) or any other image (e.g., a matplotlib figure, a static image, etc.).

To extend `Canvas`, simply create a new class that overrides the `render` method. For instance, the `RenderGymEnv` class is defined as follows:

```python
class RenderGymEnv(Canvas):
    def render(self, model):
        canvas = model.env.render()
        canvas = Image.fromarray(canvas)
        return PIL2base64(canvas)
```

The `Canvas` module expects the render output to be a `base64` string. A PIL image can be converted to this format using `PIL2base64`. If you have a matplotlib figure, use `fig2PIL` followed by `PIL2base64`.

### Settings and Performance
Upon running SimplePyDash, you will find a `Settings` dropdown menu in the navigation bar in your web browser. Here, you can specify the desired FPS . Note that while WebSocket will attempt to maintain the specified rate, it's not guaranteed to always match it.

By default, SimplePyDash runs one iteration of the `Model` object, computes the result for each dashboard component, and renders the result in the browser. To boost performance, you can perform multiple `Model` iterations and computations before rendering to the browser. Adjust the `Num. Model Iters x Gfx Update` value in the Settings to do so. This could result in a massive speed up.
