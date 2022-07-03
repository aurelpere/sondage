#import sys
import os.path
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from flask import Flask
import datetime
from app.handlers.routes import configure_routes# pylint: disable=import-error,no-name-in-module
from app.handlers.routes import create_dataframe# pylint: disable=import-error,no-name-in-module
#import pytest
#import pytest_flask
import pandas as pd
#from flask_testing import TestCase
#from flask_testing import LiveServerTestCase
#import multiprocessing
#multiprocessing.set_start_method("fork")

#http://localhost:5000/?answeryes=1&answerno=0&hash=8651738539259819158


def test_get_answers_root():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert "Désolé, il y a eu un soucis avec votre requete." in response.get_data(
    ).decode("utf-8")


def test_merci():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/merci'
    response = client.get(url)
    assert response.status_code == 200
    assert "La société Matangi vous remercie de vos retours" in response.get_data(
    ).decode("utf-8")


def test_get_answers_yes():
    app = Flask(__name__)
    configure_routes(app)
    app.debug = True
    client = app.test_client()
    url = '/?answeryes=1&answerno=0&hash=780155525518856525'
    response = client.get(url)
    #assert response.status_code == 200
    assert "Souhaitez-vous nous laisser un message" in response.get_data(
    ).decode("utf-8")
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)


def test_get_answers_no():
    app = Flask(__name__)
    configure_routes(app)
    app.debug = True
    client = app.test_client()
    url = '/?answeryes=0&answerno=1&hash=316681658622392469'
    response = client.get(url)
    assert response.status_code == 200
    assert "Souhaitez-vous nous laisser un message" in response.get_data(
    ).decode("utf-8")
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)


def test_results():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=0&answerno=1&hash=780155525518856525'
    client.get(url)
    url = '/?answeryes=0&answerno=1&hash=316681658622392469'
    client.get(url)
    df = pd.read_csv('media/results.csv', sep=';')
    assert df.loc[0, 'oui'] == 0
    assert df.loc[0, 'non'] == 2
    assert df.loc[0, 'reponses'] == 2
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)


def test_a_vote():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=1&answerno=0&hash=780155525518856525'
    client.get(url)
    url = '/?answeryes=0&answerno=1&hash=316681658622392469'
    client.get(url)
    df = pd.read_csv('media/a_vote.csv', sep=';')
    assert df.loc[1, 'oui'] == 1
    assert df.loc[1, 'hash'] == 780155525518856525
    assert df.loc[2, 'non'] == 1
    assert df.loc[2, 'hash'] == 316681658622392469
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)


def test_get_answers_double_vote():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=0&answerno=1&hash=780155525518856525'
    response = client.get(url)
    url = '/?answeryes=0&answerno=1&hash=780155525518856525'
    response = client.get(url)
    assert response.get_data(
    ) == b"Vous avez d\xc3\xa9j\xc3\xa0 vot\xc3\xa9 ou votre mail n'est pas pr\xc3\xa9sent dans la base."
    assert response.status_code == 200
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)


def test_get_answers_wronginput():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=1&answerno=1&hash=780155525518856525'
    response = client.get(url)
    assert response.get_data(
    ) == b'D\xc3\xa9sol\xc3\xa9, il y a eu un soucis avec votre requete.'
    assert response.status_code == 200


def test_get_answers_wronghash():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/?answeryes=1&answerno=0&hash=123'
    response = client.get(url)
    assert response.get_data(
    ) == b"Vous avez d\xc3\xa9j\xc3\xa0 vot\xc3\xa9 ou votre mail n'est pas pr\xc3\xa9sent dans la base."
    assert response.status_code == 200


def test_dataframe():
    df = create_dataframe(1, 0, 1)
    assert df.loc[0, 'oui'] == 1
    assert df.loc[0, 'non'] == 0
    assert df.loc[0, 'reponses'] == 1


def test_post_retour_content():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    response = client.post('/?answeryes=1&answerno=0&hash=780155525518856525',
                           data={'content': 'test'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert response.get_data(
    ) == b'La soci\xc3\xa9t\xc3\xa9 Matangi vous remercie de vos retours'
    dfretours = pd.read_csv('media/retours.csv',
                            sep=';',
                            dtype={
                                'hash': 'str',
                                'retours': 'str'
                            })
    assert "test" in dfretours['retours'].values
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)
    dfretours = pd.DataFrame({'hash': 'init', 'retours': 'init'}, index=[0])
    dfretours.to_csv('media/retours.csv', sep=';', index=False)


def test_retours():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    client.post('/?answeryes=1&answerno=0&hash=780155525518856525',
                data={'content': 'test'},
                follow_redirects=True)
    response = client.get('/retours.csv')
    assert response.status_code == 200
    assert "test" in response.get_data().decode("utf-8")
    avote = pd.DataFrame({
        'oui': 1,
        'non': 0,
        'hash': '8651738539259819158'
    },
                         index=[0])
    avote['hash'] = avote['hash'].astype('str')
    avote.to_csv('media/a_vote.csv', sep=';', index=False)
    df = pd.DataFrame({'oui': [0], 'non': [0], 'reponses': [0]})
    df.to_csv('media/results.csv', sep=';', index=False)
    dfretours = pd.DataFrame({'hash': 'init', 'retours': 'init'}, index=[0])
    dfretours.to_csv('media/retours.csv', sep=';', index=False)


def test_result():
    app = Flask(__name__)
    configure_routes(app)
    app.debug = True
    client = app.test_client()
    url = '/results.png'
    response = client.get(url)
    assert response.status_code == 200
    assert os.path.exists('media/results.png')
    file_timestamp = os.path.getmtime('media/results.png')
    now_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    assert now_timestamp - file_timestamp < 1
