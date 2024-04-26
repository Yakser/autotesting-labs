# autotesting-labs

![Linters](https://github.com/yakser/autotesting-labs/actions/workflows/linters.yml/badge.svg)

## Usage

Create venv and install dependencies:

- Windows:
    ```bash
    python -m virtualenv --python=3.12 venv
    ./venv/Scripts/activate
    pip install poetry
    poetry install
    ```
  
- Linux/MacOS:
    ```bash
    python -m virtualenv --python=3.12 venv
    source venv/bin/activate
    pip install poetry
    poetry install
    ```

- Or create venv using poetry (python 3.12 and poetry should be already installed):
  ```bash
  poetry shell
  ```

Run tests:

```bash
pytest --driver Firefox -n <NUM_OF_WORKERS> --alluredir=./allure-reports
```

Example: 

```bash
pytest --driver Firefox -n 5 --alluredir=./allure-reports
allure serve ./allure-reports
```

## Allure reports

![img.png](img/img.png)

When test fails:

![img.png](img/img_2.png)
![img_1.png](img/img_1.png)
