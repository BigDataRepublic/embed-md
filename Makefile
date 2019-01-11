
package:
	mkdir -p package
	pip3 install --target package markdown jinja2

build: package
	cp lfunction.py package
	cp index.html package
	cp -r templates package
	cd package && zip -r ../function.zip .
