.PHONY: install test demo verify build clean

install:
	python -m pip install -e .

test:
	python -m unittest discover -s tests -p 'test_*.py' -v

demo:
	python -m governed_growth_workbench run \
		--profiles examples/profiles.synthetic.json \
		--rules config/rules.synthetic.json \
		--output build/opportunities.json \
		--audit-output build/audit-events.json

verify:
	python -m compileall -q src tests
	python -m governed_growth_workbench verify-publication --root .
	$(MAKE) test
	$(MAKE) demo

build:
	python -m build

clean:
	python -c "from pathlib import Path; import shutil; [shutil.rmtree(p, ignore_errors=True) for p in map(Path, ('build', 'dist'))]"
