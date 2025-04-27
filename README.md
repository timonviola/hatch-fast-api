# fibonacci-api
The FastAPI app implements a minimal Fibonacci sequence calculator. The purpose of the repo is to show-case:
- building with hatch/uv
- property based testing

[![PyPI - Version](https://img.shields.io/pypi/v/fibonacci-api.svg)](https://pypi.org/project/fibonacci-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fibonacci-api.svg)](https://pypi.org/project/fibonacci-api)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Fibonacci-api
- get the n-th number in Fibonacci sequence
- get the `[1,Nth]` range of numbers in Fibonacci sequence (default pagination: `100`)
- add/remove sequence numbers to a exclude-list, these numbers will be redacted from the responses. The list is stored in-memory application state.

## Running the application

The following command launches the API on localhost:8000
```sh
$ hatch run dev 
```

API Documentation:
http://localhost:8000/docs#/

Run tests:

```sh
$ hatch test 
```

Run in container:
```sh
$ podman compose up 
```
## Deployment

### Scaling
- Using an orchestration tool e.g.: Kubernetes, make sure the application starts with a single `uvicorn` process. [Ref](https://fastapi.tiangolo.com/az/deployment/docker/#replication-number-of-processes)
- Using a single container, use `gunicorn`

## License

`fibonacci-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Contributing
### testing
- unit tests
- integration/e2e tests
- simulations tests and fuzzing (e.g: [https://github.com/KissPeter/APIFuzzer](https://github.com/KissPeter/APIFuzzer), [https://testdriven.io/blog/fastapi-hypothesis/](https://testdriven.io/blog/fastapi-hypothesis/))
### packaging
- hatch (+uv) is used for packaging and dependency management
### Code quality
- type checking is set to strict
- basedpyright and ruff are used for linting
- mypy is used for static type checking
- ruff is used for formatting

