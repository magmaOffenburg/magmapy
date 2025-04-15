# magma python

Python implementation of the magma agent framework.

## Getting Started

Clone the repository somewhere:

```bash
git clone git@git.hs-offenburg.de:sglaser/magmapy.git
```

### Build System

I'm experimenting with [hatchling](https://hatch.pypa.io) as a build system (no clue if it is a good choice or not, but that's what it is at the moment).

Hatchling is somehow managing some virtual environments in the background, which are used to run tests, etc. but also for running scripts of the package itself. Check out the [Docs](https://hatch.pypa.io/dev/tutorials/environment/basic-usage/) for more information.

So, in order to use hatchling, you need to install it:

```bash
pip3 install hatchling
```

### Default Development Environment(s)

Navigate to the project directory (containing the _pyproject.toml_ file) and create the default virtual environment(s) via:

```bash
hatch env create
```

Hatchling will create the default virtual environment and install the package in dev-mode as well as its dependencies.

### Type Checking and Formatting

This project heavily relies on type hints.
You can run a mypy type checking with the following command:

```bash
hatch run types:check
```

Which will effectively execute the "check" command, defined in the _pyproject.toml_ file in the "types" environment (in which mypy is installed).

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

from magma.agent.decision.behavior import Behavior
from magma.agent.model.robot.actuators import Motor
from magma.soccer_agent.model.soccer_agent import PSoccerAgentModel

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
