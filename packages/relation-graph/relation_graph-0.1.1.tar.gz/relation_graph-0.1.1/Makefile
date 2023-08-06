
test: dev
	python -m unittest tests/test_*.py

dev:
	maturin develop

release:
	docker run --rm -v $(PWD):/io ghcr.io/pyo3/maturin build --release

# TESTING

DB = ../semantic-sql/db
tests/input/all-%.csv: $(DB)/%.db
	sqlite3 -cmd ".headers on" -separator ',' $< "SELECT subject,predicate,object FROM edge UNION SELECT subject, predicate, object FROM statements WHERE predicate='rdf:type' AND subject NOT LIKE '_:%'" > $@
.PRECIOUS: tests/input/all-%.csv

tests/output/test-%.csv: tests/input/all-%.csv
	(time python -m relation_graph.runner $< -o $@) >& $@.LOG
