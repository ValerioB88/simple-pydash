## SimplePyDash
<img src="demo.gif">

A simple and modular dashboard that runs directly in the browser. Designed for real time plotting using only Python, with simplicity as its main aim.

This was originally designed to be used in conjunction with OpenAI Gym Environments, to plot agent's behaviour in real time. It's still great for that, but it can be used for many other cases.


It uses [FastAPI](https://fastapi.tiangolo.com/) web framework and uses [WebSocket](https://en.wikipedia.org/wiki/WebSocket) for two-ways communication.

#### Requirements:
`pip install fastapi "uvicorn[standard]"`

I suggest also installing `gym` if you want to see how to implement gym env in it:
`pip install gym`
This is only used in an the `examples/openai_gym.py` and is otherwise not required. 

### Installation
To install you can _either_:
- run `pip install git+https://github.com/ValerioB88/browser-dashboard.git`

**OR**
- clone/fork the repo, then install in editable mode (do this if you plan to change stuff): `pip -e {cloned folder}`  
 
### Examples 
The best way to getting started is to take a look at the examples: `examples/openai_gym.py` requires a gym library and it will plot a gym environment. `examples/generic.py` does not require a gym library.  

Run it with:
`cd {repo folder}; python -m examples.gym`. The script will try to use the first available port starting at `8000`. Open your browser at `localhost:8000` (or the used port, indicated in the output of the console).

**If you are running the script on a server**, you need to do port forwarding. Open a new terminal on your local machine and type `ssh -L {portnum}:localhost:{portnum} {username}@{machinename}`, e.g. `ssh -L 8000:localhost:8000 val@titan.it`. Then open the browser at `localhost:8000`, and you should see the dashboard.

### Getting Started 
SimplePyDash organizes your dashboard into columns, 2 by default.  The main object `CustomAPI` will take a `model_obj` and a series of `DashboardComponents`. The user-defined model is a simple iterator which does the computation, e.g. runs a neural network and returns an action. The `DashboardComponents` are widgets that can be plotted in the browser. I provide several defaults widgets that should be enough for many cases: `HeatMap`, `LinePlot`, `StaticImage`, `TextInfo`, and `RenderGymEnv`. The `plot` widgest such as `HeatMap` and `LinePlot` are based on the graphic library [Plotly](https://plotly.com/python/). This means that it's really easy to add some Plotly graph to you widget list. 

Let's take a look at a simple declaration of a `CustomAPI` object:
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
We'll talk about the `model_obj` in a second. For now consider the `dash_comps` (DashComponents). We provide 3 components, and organize them in 3 different columns, as specified by the fact that their `location_col_idx` is 0, 1, 2. `SimplePyDash` automatically creates a dashboard with 3 columns. If the `location_col_idx` of the `AppendLinePlot` was `=1`, this would automatically create 2 columns, and place the `GeneralTextInfo` widget in the first one, and the `HeatMap` and `AppendLinePlot` in the second column. Notice that the order in which the widgets are placed in a column corresponds to the order they are passed to `dash_comps`. 

Each `DashComponent` will have a default `width` and `height`. However, you can modify one or both of them to make the widget bigger or smaller. This will not resize the whole column. 

### Model
The `Model` must be an infinite iterator. Inside it, it will compute stuff that you want to plot.
 This is an example of a model for any gym environment (passed through the `env` parameter):

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

### Plotting Dashboard Components
`HeatMap` and `AppendLinePlot` are plotting components. They expect a `get_new_data_fun`, a Callable that returns the data to plot. Since a LinePlot can have multiple lines, and at each iteration you can add one or more datapoints to each line, the input to `AppendLinePlot` is a list of list: as many list as the lines, each list containing as many datapoints as you want to add. The `HeatMap` is just expecting a matrix. 


#### Canvas
The `Canvas` module returns an image, which can be used for obtaining animation in the browser. This could be the openAI rendering (`RenderGymEnv` module) or any other image (e.g. a matplotlib figure, a static image, etc).

Extending `Canvas` is extremely easy. You can see how simple is to plot something new by looking at the `RenderGymEnv` class: 

```python
class RenderGymEnv(Canvas):
    def render(self, model):
        canvas = model.env.render()
        canvas = Image.fromarray(canvas)
        return PIL2base64(canvas)
```


The `Canvas` module always expects the render output to be a `base64` string. You can convert a PIL image with `PIL2base64`. If you have a matplotlib figure use the `fig2PIL` and then the `PIL2base64`.



### Settings and Speeding Up
When you run the browser dashboard, you will see in the navigation bar on top a `Setting` dropdown menu. Here you can specify the requested FPS. Notice that the WebSocket will do its best to keep up with the indicated number, but it's not guarantee to actually match it. 
By default, `SimplyPyDash` will (1) run one iteration of the model object, (2) compute the result for each dashboard component, (3) render the result in the browser. However, to speed up the rendering more, you might want to perform (1) and (2) multiple times before passing the data to the web browser. To do that, change the `Num. Model Iters x Gfx Update` value in the Settings. This can speed up the simulation ad lot.
