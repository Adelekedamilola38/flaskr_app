# Flaskr Application

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

flask --app flaskr run --debug

pytest

coverage run -m pytest
coverage report
