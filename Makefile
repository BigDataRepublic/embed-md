
package:
	mkdir -p package
	pip install --target package markdown jinja2

build: package
	cp lfunction.py package
	cp index.html package
	cd package && zip -r ../function.zip .
