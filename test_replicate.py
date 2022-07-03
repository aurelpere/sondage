from distutils.dir_util import copy_tree
from pathlib import Path
import distutils.dir_util
import shutil
import os
import os.path
import pandas as pd
from replicate import replicate
from replicate import make_docker_nginx
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
def test_replicate():
    os.system('touch name.csv')
    replicate ('name',1)
    assert os.path.isdir('name')
    with open ('name/Dockerfile','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "COPY --chown=kr1p:kr1p name ." in txt
    with open ('name/tests/test_routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "name.handlers.routes" in txt
    with open ('name/handlers/routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "name.csv" in txt
    with open ('name/gunicorn.conf.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "0.0.0.0:5001" in txt
    shutil.rmtree('./name',ignore_errors=True)
    os.remove('name.csv')

def test_make_docker_nginx():
    os.system('touch test1.csv')
    os.system('touch test2.csv')
    make_docker_nginx(['test1','test2'])
    assert os.path.isdir('test1')
    assert os.path.isdir('test2')
    with open ('test1/Dockerfile','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "COPY --chown=kr1p:kr1p test1 ." in txt
    with open ('test1/tests/test_routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "test1.handlers.routes" in txt
    with open ('test1/handlers/routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "test1.csv" in txt
    with open ('test1/gunicorn.conf.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "0.0.0.0:5000" in txt
    shutil.rmtree('./test1',ignore_errors=True)
    with open ('test2/Dockerfile','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "COPY --chown=kr1p:kr1p test2 ." in txt
    with open ('test2/tests/test_routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "test2.handlers.routes" in txt
    with open ('test2/handlers/routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "test2.csv" in txt
    with open ('test2/gunicorn.conf.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert "0.0.0.0:5001" in txt
    shutil.rmtree('./test2',ignore_errors=True)
    with open ('docker-compose.yml','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert """---
version: '3.7'
services:
  nginx:
    build:
      context: .
      dockerfile: ./nginx/Dockerfile
    restart: always
    ports:
      - 80:80
    depends_on:
      - avocat10
      - avocat20
      - avocat30
      - avocat40
      - psy10
      - psy20
      - psy30
      - psy40
      - med10
      - med20
      - med30

  test1:
    container_name: test1
    build:
      context: .
      dockerfile: ./test1/Dockerfile
    volumes:
      - test1:/test1/media
    ports:
      - 4000:5000


  test2:
    container_name: test2
    build:
      context: .
      dockerfile: ./test2/Dockerfile
    volumes:
      - test2:/test2/media
    ports:
      - 4001:5001


volumes:
  test1:
    name: test1

  test2:
    name: test2""" in txt
    with open ('nginx/nginx.conf','r',encoding='utf-8') as fileo:
        txt=fileo.read()
    assert """
server {
    listen 80;
    server_name localhost; 

    location /test1 {
        proxy_pass http://test1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr; 
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Script-Name /test1;
        client_max_body_size 20M;
      }

    location /test2 {
        proxy_pass http://test2:5001/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr; 
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Script-Name /test2;
        client_max_body_size 20M;
      }

    
    }
""" in txt
    os.remove('test1.csv')
    os.remove('test2.csv')
if __name__ == '__main__':
    print('main')