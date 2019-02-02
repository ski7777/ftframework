# ftframework
ftframework is desiged for controlling big fischertechnik models with multiple computers (fischertechnik TXT controllers, Raspberry Pis, normal desktop computers, ...).
All computers (server and all clients) are using the same codebase, configuration file and extensions.

To start a new project just create an empty folder and place the configuration file `config.json`:
```json
{
  "clients": {
    "testclient": {
      "peripherals": {
        "complex": {
          "printer0": {}
        }
      }
    }
  },
  "peripherals": {
    "complex": {
      "printer0": {
        "builtin": true,
        "path": "Print",
        "name": "Print"
      }
    }
  }
}

```

This configuration defines one client called `testclient` and a *complex peripheral* `printer0`. `printer0` is added to `testclient`.
In this simple configuration the `server` part is missing, so the server is running on localhost port 4711.

Now we need a server script `server.py`:
```python
import time

from ftframework.Server import Server

server = Server("config.json")

while True:
    server.printer0.show("Hello World!")
    time.sleep(1)
```

All peripherals are attributes of the server object and all their calls are directly available.

Now you can start the server by running `python3 server.py` and in another shell run the client by `python3 ftFrameworkClient.py --name testclient config.json`.

For more complex configuration check the source code or wait for more documentation.
