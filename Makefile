
package:
	mkdir -p package
	pip install --target package markdown

build: package
	cp lfunction.py package
	cp index.html package
	cd package && zip -r ../function.zip .
