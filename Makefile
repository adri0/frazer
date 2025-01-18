pack:
	rm -rf package
	mkdir package
	pip install -r requirements.txt --target=package/ --platform=manylinux2014_aarch64 --implementation=cp --only-binary=:all:
	cp -r frazer package/
	cp app.py package/
	rm -f deployment-package.zip
	cd package/
	zip -r ../deployment-package.zip .
	cd ..