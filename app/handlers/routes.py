from flask import request, make_response, render_template, flash, redirect, url_for

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import io

matplotlib.use('Agg')  #to avoid gui


#http://localhost:5000/psy/?answeryes=1&answerno=0&hash=x
def create_dataframe(yes, no, rep):
    df = pd.DataFrame({
        'oui': [yes],
        'non': [no],
        'reponses': [rep],
    })
    return df


def configure_routes(app):
    #df=pd.DataFrame({'oui':[0],'non':[0],'reponses':[0]})
    #df.to_csv('results.csv',sep=';',index=False)
    #dfretours=pd.DataFrame({'hash':'init','retours':'init'},index=[0])
    #dfretours.to_csv('retours.csv',sep=';',index=False)
    #avote=pd.DataFrame({'oui':1,'non':0,'hash':'8651738539259819158'},index=[0])
    #avote['hash']=avote['hash'].astype('str')
    #avote.to_csv('a_vote.csv',sep=';',index=False)

    @app.route('/', methods=['GET', 'POST'])
    def get_answers():
        if request.method == 'POST':
            content = request.form['content']
            hash_ = request.args.get('hash')
            if not content:
                flash('Il faut remplir le champ pour soumettre un retour')
                return render_template('thanks.html')
            else:
                dfretours = pd.read_csv('media/retours.csv',
                                        sep=';',
                                        dtype={
                                            'hash': 'str',
                                            'retours': 'str'
                                        })
                df1retour = pd.DataFrame({
                    'hash': hash_,
                    'retours': content
                },
                                         index=[0])
                dftot = pd.concat([dfretours, df1retour], ignore_index=True)
                dftot.to_csv('media/retours.csv', sep=';', index=False)
                return redirect(url_for('merci',_external=True))
        # pylint: disable=global-statement

        answeryes = request.args.get('answeryes')
        answerno = request.args.get('answerno')
        hash_ = request.args.get('hash')
        df = pd.read_csv('media/results.csv', sep=';')
        n_yes = df.loc[0, 'oui']
        n_no = df.loc[0, 'non']
        n_rep = df.loc[0, 'reponses']
        if (answeryes == "1" and answerno == "0") or (answeryes == "0"
                                                      and answerno == "1"):
            mail = pd.read_csv('sondageX.csv', sep=';', dtype={'hash': 'str'})
            avote = pd.read_csv('media/a_vote.csv',
                                sep=';',
                                dtype={
                                    'hash': 'str',
                                    'oui': 'int',
                                    'non': 'int'
                                })
            if str(hash_) in mail['hash'].values and str(
                    hash_) not in avote['hash'].values:
                n_rep += int(answeryes) + int(answerno)
                n_yes += int(answeryes)
                n_no += int(answerno)
                df = pd.DataFrame({
                    'oui': [n_yes],
                    'non': [n_no],
                    'reponses': [n_rep]
                })
                df.to_csv('media/results.csv', sep=';', index=False)
                df1_a_vote = pd.DataFrame({
                    'oui': [n_yes],
                    'non': [n_no],
                    'hash': [hash_]
                })
                df_a_vote_tot = pd.concat([avote, df1_a_vote],
                                          ignore_index=True)
                df_a_vote_tot.to_csv('media/a_vote.csv', sep=';', index=False)
                return render_template('thanks.html')
            else:
                return "Vous avez déjà voté ou votre mail n'est pas présent dans la base."
        else:
            return "Désolé, il y a eu un soucis avec votre requete."

    @app.route('/merci', methods=['GET'])
    def merci():
        return "La société Matangi vous remercie de vos retours"

    @app.route('/retours.csv', methods=['GET'])
    def retours():
        df = pd.read_csv('media/retours.csv', sep=';')
        table = df.to_html()
        return table

    @app.route('/results.png', methods=['GET'])
    def get_result():
        df = pd.read_csv('media/results.csv', sep=';')
        n_yes = df.loc[0, 'oui']
        n_no = df.loc[0, 'non']
        n_rep = df.loc[0, 'reponses']
        df = create_dataframe(n_yes, n_no, n_rep)
        snsplot = sns.barplot(data=df)
        fig = snsplot.get_figure()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.savefig('media/results.png')
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.mimetype = "image/png"
        return response
