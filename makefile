
test-vulnerability:
	echo "\nmake test-vulnerability\n" &&\
	trivy fs --severity HIGH,CRITICAL . 

test-misconfiguration:
	echo "\nmake test-misconfiguration\n" &&\
	trivy config --severity HIGH,CRITICAL .

install:
	echo "\nmake install\n" &&\
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	echo "\nmake format\n" &&\
	cd app &&\
	yapf -ir -vv --style pep8 .

yamllint:
	yamllint -c yml_lint.yml .

lint:
	echo "\nmake lint\n" &&\
	pylint app --verbose --disable=R,C -sy

testapp:
	echo "\nmake testapp\n" &&\
	cd app &&\
	 pytest -vv . --cov=. --cov-report xml:reports/coverage/coverage.xml

coverage_badge:
	echo "\nmake coverage_badge\n" &&\
	cd app &&\
	 genbadge coverage

cleaning:
	echo "\nmake cleaning\n" &&\
	cd app &&\
	 rm -rf app/reports
replicate:
	python3 replicate.py

testreplicate:
	pytest -vv test_replicate.py 
	
deploy:
	echo "\nmake deploy\n" &&\
	chmod +x auto_deploy.sh &&\
	./auto_deploy.sh
	date
	cat ./ip.txt

docker:
	docker-compose build --no-cache
	docker-compose up -d

all: test-vulnerability test-misconfiguration install format yamllint lint testapp cleaning replicate testreplicate deploy
