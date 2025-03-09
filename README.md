This is a simple engine for gamebooks.

# How it works?

A gamebook scenario can be represented as a graph containing scenario moves as nodes and scenario paths as edges. This
graph is represented in code with the ScenarioMove and ScenarioWay classes. Each scenario starts with a ScenarioMove
object containing a description of the current move and the available ways to move to, and each ScenarioWay object
contains a description of the way and the next ScenarioMove object.

Check out the [examples](./examples) to see this in action.