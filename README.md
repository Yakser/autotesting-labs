# autotesting-labs

## Usage

Create venv and install dependencies:

```bash
python -m virtualenv --python=3.12 venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install poetry
poetry install
```

Run tests:

```bash
pytest --driver Firefox --driver-path /path/to/driver -n <NUM_OF_WORKERS>
```

