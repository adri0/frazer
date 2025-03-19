lambda:
	mkdir package
	uv pip install -r requirements.txt --target=package/ --python-platform=aarch64-manylinux2014 --only-binary=:all:
	cp -r frazer package/
	cp frazer/lambda.py logging.conf package/
	rm -f frazer-lambda.zip
	cd package/ ; zip -r ../frazer-lambda.zip . -x "*__pycache__*"
	rm -rf package/

build-site:
	uv run python webapp/build.py

deploy-site:
	aws s3 cp site/frazer.html s3://coisaspublicas/frazer.html --acl public-read

deploy-lambda:
	aws lambda update-function-code --function-name frazer --zip-file fileb://frazer-lambda.zip

lambda-url:
	aws lambda get-policy --function-name frazer --query "Policy" --output text | \
		grep -o 'arn:aws:execute-api:[^"]*' | sed -E 's#arn:aws:execute-api:([^:]+):[^:]+:([^/]+)/([^/]+)/([^"]+)#https://\2.execute-api.\1.amazonaws.com/\3/\4#'