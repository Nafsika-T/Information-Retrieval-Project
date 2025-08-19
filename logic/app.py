import os
from queries import close_connection
from inverted_index import retrieve_top_k_docs
from queries import fetch_speech_details, fetch_names_of_members, fetch_names_of_parties
from flask import Flask, render_template, request, jsonify
from flask import send_file

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_file(filename)


@app.route('/extract_keywords', methods=['GET', 'POST'])
def extract_keywords():
    if request.method == 'POST':
        keyword_type = request.form.get('keywordType')
        entity = request.form.get('entity')

        base_path = 'Data/parliament_data/'
        if keyword_type == 'member':
            search_path = os.path.join(base_path, 'parliament_member', entity)
        elif keyword_type == 'party':
            search_path = os.path.join(base_path, 'parliament_party', entity)
        else:
            return "Invalid keyword type", 400

        image_paths = []
        years = []
        if os.path.exists(search_path) and os.path.isdir(search_path):
            for year_folder in sorted(os.listdir(search_path)):
                year_path = os.path.join(search_path, year_folder)
                if os.path.isdir(year_path):
                    image_file = os.path.join(year_path, f"{year_folder}.png")
                    if os.path.exists(image_file):
                        image_paths.append(image_file)
                        years.append(year_folder)
        image_data = []
        for i in range(len(image_paths)):
            prev_year = years[i - 1] if i > 0 else years[-1]
            next_year = years[i + 1] if i < len(image_paths) - 1 else years[0]
            image_data.append((image_paths[i], years[i], prev_year, next_year))

        return render_template('extract_keywords.html', image_data=image_data)

    return render_template('extract_keywords.html')


@app.route('/search_speeches', methods=['POST', 'GET'])
def search_speeches():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    page = int(request.args.get('page', 1)) 
    per_page = 10 
    k = 30

    if not query:
        return render_template('search_results.html', results=[], error_message="No search term provided.", page=page, total_pages=0)

    print(f"Query: {query}, K: {k}, Page: {page}")

    try:
        top_k_docs = retrieve_top_k_docs(k, query)
        print(f"Top K Docs: {top_k_docs}")
    except Exception as e:
        print(f"Error in retrieve_top_k_docs: {e}")
        return "An internal error occurred while retrieving documents", 500

    if not top_k_docs or top_k_docs == list(range(k)):
        return render_template('search_results.html', results=[], error_message="No documents found for the given search term.", page=page, total_pages=0)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_docs = top_k_docs[start:end]

    results = []
    for doc_id in paginated_docs:
        try:
            details = fetch_speech_details(doc_id)
            if details:
                results.append(details)
        except Exception as e:
            print(f"Error in fetch_speech_details: {e}")
            continue

    total_pages = (len(top_k_docs) + per_page - 1) // per_page

    return render_template('search_results.html', results=results, query=query, page=page, total_pages=total_pages)



@app.route('/speech/<int:doc_id>')
def view_speech(doc_id):
    speech_details = fetch_speech_details(doc_id)
    if not speech_details:
        return "Speech not found", 404
    return render_template('view_speech.html', speech=speech_details)


@app.route('/top_k_similarities', methods=['GET', 'POST'])
def top_k_similarities():
    results = []
    error_message = None

    if request.method == 'POST':
        k_value = request.form.get('k')

        if not k_value:
            error_message = "Please enter a value for K."
        else:
            try:
                k = int(k_value)
                if k <= 0:
                    error_message = "The value of K must be a positive integer greater than 0."
                elif k > 100:
                    error_message = "The value of K cannot be greater than 100. Please try again with a smaller number."
                else:
                    file_path = os.path.join('Data', '100_most_similar_members.txt')
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()

                    for line in lines[:k]:
                        members, similarity = line.split(':')
                        similarity = float(similarity.strip())
                        results.append((similarity, *members.split(',')))
            except ValueError:
                error_message = "Please enter a valid integer for K."

    return render_template('top_k_similarities.html', results=results, error_message=error_message)


@app.route('/extract_topics')
def extract_topics():
    total_variance_ratio = ""
    file_path = os.path.join('Data', 'lsa_topics.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if lines[-1].startswith("Total Explained Variance Ratio:"):
        total_variance_ratio = float(lines[-1].split(":")[1].strip())
        total_variance_ratio = f"Total EVC: {total_variance_ratio * 100:.2f}%"

    return render_template('extract_topics.html', total_variance_ratio=total_variance_ratio)


@app.route('/extract_topics_action', methods=['POST'])
def extract_topics_action():
    topics = []
    file_path = os.path.join('Data', 'lsa_topics.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if lines[-1].startswith("Total Explained Variance Ratio:"):
        lines = lines[:-1]

    topic = None
    for line in lines:
        if line.startswith("Topic"):
            if topic:
                topics.append(topic)
            topic = [line.strip()]
        elif line.startswith("Explained Variance of component:"):
            variance = float(line.split(":")[1].strip())
            variance_percentage = f"EVC: <span class='evc'>{variance * 100:.2f}%</span>"
            topic.append(variance_percentage)
        else:
            topic.append(line.strip())
    if topic:
        topics.append(topic)

    topics_html = ""
    for i in range(0, len(topics), 5):
        topics_html += '<div class="row justify-content-center">'
        for topic in topics[i:i + 5]:
            topics_html += f'<div class="col-md-2"><div class="topic-card"><h3>{topic[0]}</h3><p>{"<br>".join(topic[1:])}</p></div></div>'
        topics_html += '</div>'

    return jsonify(topics_html)


@app.route('/entity_recognition', methods=['GET'])
def entity_recognition_page():
    return render_template('entity_recognition.html')


@app.route('/image/<member_dir>/ner.png')
def serve_ner_image(member_dir):
    image_path = os.path.join('Data', 'parliament_data', 'parliament_member', member_dir, 'ner.png')

    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return "Image not found", 404


@app.route('/entity_recognition', methods=['POST'])
def entity_recognition():
    data = request.json
    member = data.get('member')

    member_dir = member
    image_path = os.path.join('Data', 'parliament_data', 'parliament_member', member_dir, 'ner.png')

    print(f"Looking for image at: {image_path}")

    if os.path.exists(image_path):
        image_url = f'/image/{member_dir}/ner.png'
        return jsonify({'image_path': image_url})
    else:
        return jsonify({'image_path': None, 'message': f"No NER image found for {member}."})


@app.route('/autocomplete_entity', methods=['GET'])
def autocomplete_entity():
    query = request.args.get('q', '').lower()
    type = request.args.get('type', '')

    if type == 'member':
        names = fetch_names_of_members()
    elif type == 'party':
        names = fetch_names_of_parties()
    else:
        return jsonify([])

    print(f"Type: {type}, Query: {query}, Suggestions: {names[:5]}")

    suggestions = [name for name in names if name.lower().startswith(query)]

    return jsonify(suggestions)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    names = fetch_names_of_members()
    results = [name for name in names if name.lower().startswith(search.lower())]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
