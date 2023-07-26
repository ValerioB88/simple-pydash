/* runcontrol.js
 Users can reset() the model, advance it by one step(), or start() it. reset() and
 step() send a message to the server, which then sends back the appropriate data.
 start() just calls the step() method at fixed intervals.

 The model parameters are controlled via the ModelController object.
*/

/*
 * Variable definitions
 */
const controller = new ModelController();
const vizElements = [];
const startModelButton = document.getElementById("play-pause");
const stepModelButton = document.getElementById("step");
const resetModelButton = document.getElementById("reset");
const closeSocketButton = document.getElementById("close-socket");

/**
 * A ModelController that defines the model state.
 * @param  {number} tick=0 - Initial step of the model
 * @param  {boolean} running=false - Initialize the model in a running state?
 * @param  {boolean} finished=false - Initialize the model in a finished state?
 */
function ModelController(tick = 0, running = false, finished = false) {
  this.tick = tick;
  this.running = running;
  this.finished = finished;
  this.timeoutId = null;
  this.FPS = 10;

  document.getElementById("intervalSlider").addEventListener(
    "input",
    function (event) {
      document.getElementById("fpsValue").innerText = event.target.value;
      this.FPS = event.target.value;
    }.bind(this)
  );

  document.getElementById("IterXupdates").addEventListener(
    "input",
    function (event) {
      document.getElementById("iterValue").innerText = event.target.value;
      send({
        type: "change_server_params",
        param_name: "iters_per_gfx_update",
        value: event.target.value,
      });
    }.bind(this)
  );

  this.start = function start() {
    this.running = true;
    startModelButton.firstElementChild.innerText = "Stop";
    this.step((keep_running = true));
  };

  this.stop = function stop() {
    this.running = false;
    startModelButton.firstElementChild.innerText = "Start";

    if (this.timeoutId !== null) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
  };

  this.step = function step(keep_running) {
    this.tick += 1;

    send({ type: "get_step", step: this.tick });
    if (keep_running) {
      this.timeoutId = setTimeout(
        () => this.step(keep_running),
        1000 / this.FPS
      );
    }
  };

  this.reset = function reset() {
    this.tick = 0;
    vizElements.forEach((element) => element.reset());
    if (this.finished) {
      this.finished = false;
      startModelButton.firstElementChild.innerText = "Start";
    }
    send({ type: "reset" });
  };

  this.reset_viz = function reset_viz() {
    vizElements.forEach((element) => element.reset());
  };
  /** Stops the model and put it into a finished state */
  this.done = function done() {
    this.stop();
    this.finished = true;
    startModelButton.firstElementChild.innerText = "Done";
  };

  /**
   * Render visualisation elements with new data.
   * @param {any[]} data Model state data passed to the visualization elements
   */
  this.render = function render(data) {
    if (document.getElementById("global_renderer").checked) {
      for (let [index, element] of vizElements.entries()) {
        if (data[index] != null) {
          element.render(data[index]);
        }
        // vizElements.forEach((element, index) => element.render(data[index]));
      }
    }
  };
}

/*
 * Button logic for start, stop and reset buttons
 */
startModelButton.onclick = () => {
  if (controller.running) {
    controller.stop();
  } else if (!controller.finished) {
    controller.start();
  }
};
stepModelButton.onclick = () => {
  if (controller.running) {
    controller.stop();
  }
  if (!controller.finished) {
    controller.step((keep_running = false));
  }
};
resetModelButton.onclick = () => controller.reset();

closeSocketButton.onclick = () => {
  send({ type: "close-socket" });
};

/*
 * Websocket opening and message handling
 */
/** Open the websocket connection; support TLS-specific URLs when appropriate */
const ws = new WebSocket(
  (window.location.protocol === "https:" ? "wss://" : "ws://") +
    location.host +
    "/ws"
);

/**
 * Parse and handle an incoming message on the WebSocket connection.
 * @param {string} message - the message received from the WebSocket
 */
ws.onmessage = function (message) {
  const msg = JSON.parse(message.data);
  switch (msg["type"]) {
    case "render_data_multi_iter":
      // Update visualization state
      for (let element of msg["iterations"]) {
        controller.render(element["data"]);
      }
      break;
    case "end":
      controller.done();
      break;
    case "UI_action":
      if (msg["data"] === "reset_viz_and_step") this.tick = 0;
      controller.reset_viz();
      controller.step();
      break;
    default:
      // There shouldn't be any other message
      console.log("Unexpected message.");
      console.log(msg);
  }
};

/**
 * Turn an object into a string to send to the server, and send it.
 * @param {string} message - The message to send to the Python server
 */
const send = function (message) {
  const msg = JSON.stringify(message);
  ws.send(msg);
};

document.addEventListener("keydown", function onEvent(event) {
  console.log("PRESSED");
  send({
    type: "keyboard_command",
    command: event.key,
  });
});

document.addEventListener("keydown", function onEvent(event) {
  console.log("PRESSED" + event.key);
  if (event.key === "f") {
    send({ type: "switch_fast" });
  }
});
// Backward-Compatibility aliases
const control = controller;
const elements = vizElements;
