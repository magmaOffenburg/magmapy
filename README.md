# magma python

Python implementation of the magma agent framework.

## Getting Started

Clone the repository somewhere...

### Build System

This project uses [hatch](https://hatch.pypa.io) as project management tool.  
You can install _hatch_ via your package manager or `pip install hatch` (or `pipx install hatch` on managed systems).

Hatch is managing various virtual environments in the background, which are used to run scripts, tests, etc.
You don't need to create any virtual environment by yourself.
Virtual environments are automatically created by hatch on demand (when running scripts).
The project itself and the environment specific dependencies specified in the _pyproject.toml_ file are automatically installed in these virtual environments.
Check out the [Docs](https://hatch.pypa.io/dev/tutorials/environment/basic-usage/) for more information.

### Default Development Environment(s)

Even though virtual environments are created on demand, let's create the default virtual environment(s) by running:

```bash
hatch env create
```

in the project directory (containing the _pyproject.toml_ file).
Hatch will create the default virtual environment and install the package in dev-mode as well as its dependencies.

### Type Checking and Formatting

This project heavily relies on type hints.
You can run a MyPy type checking with the following command:

```bash
hatch run types:check
```

Which will effectively execute the "check" command, defined in the _pyproject.toml_ file in the "types" environment (in which MyPy is installed).

You can also run the ruff code formatter via:

```bash
hatch fmt
```

to format the code and get some suggestions for improving your code.

### Run an RCSS Agent

The main scripts of the package are specified in the _pyproject.toml_ file.
So far, there only exists a main function for running a RCSS agent:

```bash
hatch run magma
```

With this command, hatchling will run the "magma" command within the default virtual environment.
Use the `-h` option to get some help for the command (`hatch run magma -h`).

#### Get Some Action

So far the agent doesn't do very much after connecting to the server.
In order to get something moving, you need to get some behaviors ready!

For starting, you can use this example behavior for rotating it's head:

```python
import numpy as np
import numpy.typing as npt

from magmapy.agent.decision.behavior import Behavior
from magmapy.agent.model.robot.actuators import Motor
from magmapy.soccer_agent.model.soccer_agent import PSoccerAgentModel

class MoveBehavior(Behavior):
    def __init__(self, model: PSoccerAgentModel):
        super().__init__('move')

        self._model = model

        self._velocities: npt.NDArray[np.float32] = np.sin(np.linspace(-np.pi, np.pi, 200)) * 1.0
        self._vel_idx: int = 0

    def perform(self) -> None:
        if self._vel_idx >= len(self._velocities):
            self._vel_idx = self._vel_idx % len(self._velocities)

        vel = self._velocities[self._vel_idx]
        ny_motor = self._model.get_robot().get_actuator('NeckYaw', Motor)
        if ny_motor:
            ny_motor.set(0.0, vel, 0.0, 0.0)

        self._vel_idx += 1

    def is_finished(self) -> bool:
        return bool(self._vel_idx >= self._velocities.size)
```

and call it from the decision maker.

But, in the end, there are also still a couple of gears missing in our gear box...

### Build the Projekt

You can build a release version of the package, by running:

```bash
hatch build
```

after which you will find a _dist_ directory with the build artifacts (a Python wheel and a source archive).

Executing `hatch clean` will remove the build artifacts again.
