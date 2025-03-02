lambda:
	mkdir package
	pip install -r requirements.txt --target=package/ --platform=manylinux2014_aarch64 --implementation=cp --only-binary=:all:
	cp -r frazer package/
	cp frazer/lambda.py logging.conf package/
	rm -f frazer-lambda.zip
	cd package/ ; zip -r ../frazer-lambda.zip . -x "*__pycache__*"
	rm -rf package/

build-site:
	python frontend/build.py

deploy-site:
	aws s3 --profile=frazer cp site/frazer.html s3://coisaspublicas/frazer.html --acl public-read

deploy-lambda:
	aws --profile=frazer lambda update-function-code --function-name frazer --zip-file fileb://frazer-lambda.zip

lambda-url:
	aws --profile=frazer lambda get-policy --function-name frazer --query "Policy" --output text | \
		grep -o 'arn:aws:execute-api:[^"]*' | sed -E 's#arn:aws:execute-api:([^:]+):[^:]+:([^/]+)/([^/]+)/([^"]+)#https://\2.execute-api.\1.amazonaws.com/\3/\4#'