from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response
from flask_migrate import Migrate, migrate
from models import db, Mermaids

import os
import re
import helper_functions
from MermaidPY import code_to_mermaid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datastore.db"

db.init_app(app)

migrate = Migrate(app, db)

from dotenv import load_dotenv
load_dotenv()

global SCRIPT_ROOT
SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))

mermaid_directory = os.path.join(SCRIPT_ROOT, 'Mermaid_Files')
if not os.path.exists(mermaid_directory):
    os.makedirs(mermaid_directory)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        mermaids = Mermaids.query.all()
        return render_template('home.html', mermaids = mermaids)
    
    mermaid_name = request.form.get('mermaid_name')
    mermaid_description = request.form.get('mermaid_description')

    mermaid = Mermaids(name = mermaid_name, description = mermaid_description)

    db.session.add(mermaid)
    db.session.commit()

    mermaid.folder_path = helper_functions.create_mermaid_folder(mermaid.unique_id)
    db.session.commit()

    return redirect(url_for('show_mermaid', mermaid_id = mermaid.unique_id))

@app.route('/mermaid/<mermaid_id>')
def show_mermaid(mermaid_id):
    mermaid = Mermaids.query.get(mermaid_id)
    response = make_response(render_template('show_mermaid.html', mermaid = mermaid))
    response.set_cookie('mermaid_unique_id', mermaid_id)
    return response

@app.route('/delete_mermaid', methods = ['DELETE'])
def delete_mermaid():
   unique_id = request.form.get('unique_id')
   mermaid = Mermaids.query.get(unique_id)

   helper_functions.delete_mermaid_folder(mermaid_unique_id = unique_id)

   db.session.delete(mermaid)
   db.session.commit()
   return jsonify(delete_done = True, redirect_location = url_for('home'))  

@app.route('/mermaid/<mermaid_id>/mermaid_code', methods = ['GET'])
def show_mermaidcode(mermaid_id):
    response = make_response(render_template('show_mermaid_code.html'))
    response.set_cookie('mermaid_unique_id', mermaid_id)
    return response

@app.route('/mermaid/<mermaid_id>/mermaid_render', methods = ['GET'])
def show_mermaidrender(mermaid_id):
    mermaid = Mermaids.query.get(mermaid_id)
    with open(os.path.join(mermaid.folder_path, 'mermaid_code.txt'), 'r') as file_handle:
        file_contents = file_handle.readlines()
    
    response = make_response(render_template('show_mermaid_render.html', mermaid_code = ''.join(file_contents)))
    response.set_cookie('mermaid_unique_id', mermaid_id)

    return response

@app.route('/mermaid/<mermaid_id>/view_svg', methods = ['GET'])
def view_svg(mermaid_id):
    mermaid = Mermaids.query.get(mermaid_id)
    svg_path = os.path.join(mermaid.folder_path, 'svg_render.svg')
    svg_exists = str(os.path.exists(svg_path))
    
    response = make_response(render_template('svg_preview.html'))
    response.set_cookie('mermaid_unique_id', mermaid_id)
    response.set_cookie('svg_exists', svg_exists)

    return response

@app.route('/get_file', methods = ['POST'])
def get_file():
    unique_id = request.form.get('unique_id')
    mermaid = Mermaids.query.get(unique_id)

    required_file = request.form.get('file')

    try:
        file_path = os.path.join(mermaid.folder_path, required_file)
        with open(file_path, 'r') as file_handle:
            file_contents = file_handle.readlines()

            return jsonify(result = True, file_contents = file_contents)    
    except Exception as exp:
        print(exp)
    return jsonify(result = False)

@app.route('/save_file', methods = ['POST'])
def save_file():
    unique_id = request.form.get('unique_id')
    mermaid = Mermaids.query.get(unique_id)

    required_file = request.form.get('file')

    try:
        file_path = os.path.join(mermaid.folder_path, required_file)
        with open(file_path, 'w') as file_handle:
            file_contents = request.form.get('file_contents')
            # file_contents = re.sub(r'\t{3}', '\t', file_contents)
            file_handle.writelines(file_contents)

            return jsonify(result = True)
    except Exception as exp:
        print(exp)
    return jsonify(result = False)

@app.route('/process_codefile', methods = ['POST'])
def process_codefile():
    unique_id = request.form.get('unique_id')
    mermaid = Mermaids.query.get(unique_id)

    try:
        file_path = os.path.join(mermaid.folder_path, 'codefile.txt')
        with open(file_path, 'r') as file_handle:
            file_contents = file_handle.readlines()

            flowchart = code_to_mermaid.perform_shunting_yard(text_contents = file_contents)
            mermaid_code = code_to_mermaid.flowchart_to_mermaid(flowchart = flowchart) 

            with open(os.path.join(mermaid.folder_path, 'mermaid_code.txt'), 'w') as file_handle:
                file_handle.writelines(mermaid_code)

        return jsonify(result = True)
    except Exception as exp:
        print(exp)
    return jsonify(result = False)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = "5537", debug = True)