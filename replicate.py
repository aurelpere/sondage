from distutils.dir_util import copy_tree
from pathlib import Path
import distutils.dir_util
import shutil
import os
import os.path
import pandas as pd

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
def replicate(name,idx):
    if os.path.isdir('app_mod'):
        shutil.rmtree('app_mod',ignore_errors=True)
    Path("app_mod").mkdir(parents=True, exist_ok=True)
    print('launching copytree')
    copytree("app", "app_mod")
    print('copytree launched')
    with open ('app_mod/Dockerfile','r',encoding='utf-8') as fileo:
        txt=fileo.read()
        txt=txt.replace('COPY --chown=kr1p:kr1p app .',f'COPY --chown=kr1p:kr1p {name} .')
    with open ('app_mod/Dockerfile','w',encoding='utf-8') as fileo:
        fileo.write(txt)

    with open ('app_mod/tests/test_routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
        txt=txt.replace('app.handlers.routes',f'{name}.handlers.routes')
    with open ('app_mod/tests/test_routes.py','w',encoding='utf-8') as fileo:
        fileo.write(txt)   

    with open ('app_mod/handlers/routes.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
        txt=txt.replace('sondageX',f'{name}')
    with open ('app_mod/handlers/routes.py','w',encoding='utf-8') as fileo:
        fileo.write(txt)
    with open ('app_mod/gunicorn.conf.py','r',encoding='utf-8') as fileo:
        txt=fileo.read()
        txt=txt.replace('0.0.0.0:5000',f'0.0.0.0:{5000+idx}')
    with open ('app_mod/gunicorn.conf.py','w',encoding='utf-8') as fileo:
        fileo.write(txt)
    Path(f"./{name}").mkdir(parents=True, exist_ok=True)
    copy_tree("app_mod", f"./{name}")
    shutil.copyfile(f'{name}.csv', f'{name}/{name}.csv')
    shutil.rmtree('./app_mod',ignore_errors=True)

def make_docker_nginx(namelist):
    dfinit = pd.DataFrame({'name': 'ini', 'port': 'init'}, index=[0])
    dfinit.to_csv('mapping.csv',sep=';',index=False)
    text0="""---
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
      - avocatdix
      - avocatvingt
      - avocattrente
      - avocatquarente
      - psydix
      - psyvingt
      - psytrente
      - psyquarente
      - meddix
      - medvingt
      - medtrente
"""
    text3="""
volumes:"""

    nginx0="""
server {
    listen 80;
    server_name localhost; 
"""

    nginxend="""
    
    }
"""
    aggservice=""
    aggvolume=""
    aggnginx=""
    #replicate('psy10')
    for idx, x in enumerate (namelist):
        print(f'copying {x}')
        replicate(x,idx)
        vol = """
  app:
    name: app
"""
        serv="""
  app:
    container_name: app
    build:
      context: .
      dockerfile: ./app/Dockerfile
    restart: always
    volumes:
      - app:/app/media
    ports:
      - 5000:5000

"""
        nginx1 = """
    location /app {
        proxy_pass http://app:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr; 
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Script-Name /app;
        client_max_body_size 20M;
      }
"""
        serv=serv.replace('app',x)
        serv=serv.replace('5000:5000',f'{4000+idx}:{5000+idx}')
        vol=vol.replace('app',x)
        nginx1=nginx1.replace('app',x)
        nginx1=nginx1.replace('5000',f'{5000+idx}')
        aggnginx=aggnginx+nginx1
        aggvolume=aggvolume+vol
        aggservice=aggservice+serv
        df0=pd.read_csv('mapping.csv',sep=';')
        df1=pd.DataFrame({'name':x,'port':str(4000+idx)},index=[0])
        dftot=pd.concat([df0,df1],ignore_index=True)
        dftot.to_csv('mapping.csv',sep=';',index=False)
    with open ('docker-compose.yml','w',encoding='utf-8') as fileo:
        text=text0+aggservice+text3+aggvolume
        fileo.write(text)
    with open('nginx/nginx.conf','w',encoding='utf-8') as fileo:
        text=nginx0+aggnginx+nginxend
        fileo.write(text)

if __name__ == '__main__':
    make_docker_nginx(['avocatdix','avocatvingt','avocattrente','avocatquarente','psydix','psyvingt','psytrente','psyquarente','meddix','medvingt','medtrente'])