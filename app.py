from flask import Flask, render_template, request
from flask_elasticsearch import FlaskElasticsearch


app = Flask(__name__)
es = FlaskElasticsearch(app)


@app.route('/')
def index():
    return render_template('index.html', a = 5)


@app.route('/result', methods = ['POST'])
def form():
    if request.method == 'POST':
        text_query = request.form['text']
        query = {
            'query' : {
                'match_phrase' : {
                    'textBody' : {
                        'query' : text_query,
                        'slop' : 2
                    }
                }
            }
        }
        result = es.search(index = 'lande', body = query)['hits']['hits']
        if len(result) > 0:
            return render_template('articles.html', m = result)
        else:
            return 'Таких записей нет!'


if __name__ == '__main__':
    app.run(debug = True)
