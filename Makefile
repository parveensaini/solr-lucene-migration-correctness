venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r scripts/requirements.txt

up:
	bash scripts/up.sh

reset:
	bash scripts/reset.sh

wait:
	bash scripts/wait_for_solr.sh

load:
	bash scripts/load.sh corpus/docs.json

# Run all pairs (5v8, 8v9, 5v9)
diff: venv
	. .venv/bin/activate && python scripts/diff.py corpus/queries.json reports

# Run a single pair
diff-5v8: venv
	. .venv/bin/activate && PAIR=5v8 python scripts/diff.py corpus/queries.json reports

diff-8v9: venv
	. .venv/bin/activate && PAIR=8v9 python scripts/diff.py corpus/queries.json reports

diff-5v9: venv
	. .venv/bin/activate && PAIR=5v9 python scripts/diff.py corpus/queries.json reports

bootstrap: reset wait load

all: reset wait load diff
