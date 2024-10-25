import os
from flask import Flask, render_template, request, jsonify

from utils.utils import *
from utils.mysqlite import MySqlite

app = Flask(__name__)

# index page
@app.route('/<int:page>', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index(page=1):
    my_sqlite = MySqlite()
    per_page = 30  # 每页显示的记录数
    sql = 'SELECT * FROM rem_table LIMIT ? OFFSET ?' 
    if request.method == 'POST':
        searchOption = request.form['option']
        searchKey = request.form['keyword']
        if searchOption == '1':
            search_col = 'Carrier_Name'
        elif searchOption == '2':
            search_col = 'Agent_Name'
        elif searchOption == '3':
            search_col = 'Earner_Type'
        elif searchOption == '4':
            search_col = 'Commission_Period'

        sql = 'SELECT * FROM rem_table WHERE ' + search_col + ' LIKE "%' + searchKey + '%"'
        table_data = my_sqlite.db_query(sql)
        return jsonify({'table_data': table_data})
    
    table_data = my_sqlite.db_query(sql, (per_page, (page - 1) * per_page))
    return render_template('index.html', table_data=table_data, page=page, total_pages=1500)

# upload file
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'})

    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join('./data', file.filename)
        file.save(file_path)
        df = parse_data(file.filename)
        save_data_sqlite(df)
        return jsonify({'error': 'upload success'})

# export file
@app.route('/export_file', methods=['GET'])
def export_file():
    export_data()
    return jsonify({'error': 'upload success'})

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        params = request.form.get('option')
        top_data = find_top(params)
        return jsonify({'table_data': top_data})
    return render_template('analysis.html')


if __name__ == '__main__':
    app.run(debug=True)