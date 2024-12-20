# Setup

## Install dependencies

- Dependencies:
    - Python 3.11
    - `uv` package manager
    - Packages:
        - `kafka-python==2.0.2`
        - `pyyaml==6.0.2`
        - `flask==3.1.0`

- We use [`uv`](https://docs.astral.sh/uv/) as our Python package manager.
    - To install the `uv` package manager, follow the instructions on the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
```

## Enter the virtual environment

```bash
source .venv/bin/activate
```
