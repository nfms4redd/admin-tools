build:
	@tar -czf admin-scripts.tgz *.sh *.py

test: 
	@python -m unittest discover -t . -p "*_test.py"
	
clean:
	@rm -rf *.pyc tests/*.pyc admin-scripts.tgz
