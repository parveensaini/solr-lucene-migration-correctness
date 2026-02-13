venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r scripts/requirements.txt

up:
	bash scripts/up.sh

reset:
	bash scripts/reset.sh

load:
	bash scripts/load.sh corpus/docs.json

diff: venv
	. .venv/bin/activate && python scripts/diff.py corpus/queries.json reports

all: reset load diff

