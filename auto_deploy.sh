#!/bin/sh
trap 'exit' ERR
cd ..&& tar -cvf project.tar sondage

echo 'uploading/copying with scp -i /Users/macbook/github/digitalocean ./project.tar kr1p@server:/tmp/project.tar'
cd sondage && scp -P 4444 -i /Users/macbook/github/digitalocean ../project.tar kr1p@$(cat ./ip.txt | sed 's/"//g'):/tmp/project.tar


echo 'Uploaded complete.'

echo 'ssh and building docker into server ...'
ssh -p 4444 -i /Users/macbook/github/digitalocean kr1p@$(cat ./ip.txt | sed 's/"//g') << 'ENDSSH'
	echo 'extracting tar file'
    sudo rm -rf /sondage/* && sudo tar -xf /tmp/project.tar -C /
	echo 'tar file extracted'		
	echo 'configuring for python package fine deployment'
	sudo chown -R kr1p /sondage
	sudo chmod -R u=rwx /sondage
	export PATH="/home/kr1p/.local/lib/python3.9/site-packages:$PATH"
	echo 'configuring done'
	echo 'going into sondage folder'	
    cd /sondage
	echo 'getting rid of hidden macos files'
	sudo find . -type f -name '._*' -delete 
	echo 'hidden macos files deleted'
	echo 'making install'
	cd /sondage/app
	make install
	echo 'install done'
	echo 'running format'
	make format
	echo 'format done'
	echo 'running lint'
	make lint
	echo 'lint done'
	echo 'running test'
	make test
	echo 'test done'
	cd /sondage
	echo 'replicating'
	python3 replicate.py
	echo 'replicating done'
	echo 'running docker'
	docker-compose build
	docker-compose up -d
	echo 'docker done'	
	#echo 'running vulnerability check'
	#trivy fs --severity HIGH,CRITICAL --security-checks vuln / > security_check.txt
	#echo 'vuln check done'
	
ENDSSH
echo 'Build complete.'
echo 'removing project.tar'
rm project.tar
echo 'project.tar removed'

