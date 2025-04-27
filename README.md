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
- add/remove sequence numbers to a block-list, these numbers will be redacted from the responses. The list is stored in-memory application state.

## License

`fibonacci-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
