from os import link
from flask import Flask, render_template, request

from pymongo import MongoClient

app = Flask(__name__)

cluster = MongoClient('mongodb+srv://priyanka:oeFD1PBhw9J0hp0z@cluster0.s4pws.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# Database name
db = cluster['paper']

# Collection name
collection = db['paper_review']
score = db['score']
    
@app.route('/')
def my_form():
    
    return render_template('submit.html')


@app.route("/", methods=["GET", "POST"])
def submit():
    
    title       = request.form.get('title')
    paper_link  = request.form.get('paper_link')
    # print(f"\n\nTitle : {title} \t Paper Link : {paper_link}\n\n")

    collection.insert_one(
        {'title': title, 'paper_link': paper_link})

    return render_template('submit.html')

@app.route('/papers')
def choose_paper():
    
    all_links = collection.find({})
    result = []
    for data in all_links:
        del data['_id']
        result.append(data)
        
    
    return render_template('papers.html', result = result)


@app.route("/review", methods=['POST' , 'GET'])


def review():

    if request.method == 'POST':

        title           = request.form.get('title')
        category        = request.form.get('category')
        context         = request.form.get('context')
        correct         = request.form.get('correct')
        contributions   = request.form.get('contributions')
        clarity         = request.form.get('clarity')
        overall_score   = request.form.get('overall_score')

        paper = collection.find({"title": title})

        try:

            for item in paper:
                paper_id = item['_id']
                current_data = { 'ref': paper_id, 'category': category, 'context': context, 'correct': correct,
                                    'contributions': contributions, 'clarity': clarity, 'overall_score': overall_score}
                score.insert_one(current_data)
        
        except:
            return "Paper Doesn't Exist"
        
    return render_template('review.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")