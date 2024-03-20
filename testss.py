
import time
from datetime import datetime

from py2neo import Graph

from flask import Flask, jsonify, request



app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)





@app.route('/', methods=['GET'])
def get_lab1():

    course = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    date_object1 = datetime.strptime(start_date, "%Y-%m-%d")
    unix_time1 = time.mktime(date_object1.timetuple())/60/60/24
 
    date_object2 = datetime.strptime(end_date, "%Y-%m-%d")
    unix_time2 = time.mktime(date_object2.timetuple())/60/60/24
    d1 = int(unix_time1) + 1
    d2 = int(unix_time2) + 1
    try:
        volumes = get_class_volumes(course, d1, d2)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    dict_volumes = [{'class_title':volumes[0][i], 'date':volumes[1][i], 'pair_number':volumes[2][i], 'volume':volumes[3][i]} for i in range(len(volumes[0]))]
    
    return jsonify({'volumes': dict_volumes}), 200







def get_class_volumes(title:str, start_date:str, end_date:str) -> list:
    neo4j_graph = Graph("bolt://localhost:7687")
    query = f"""MATCH (c:Course {{title: "{title}"}})-[:HAS_CLASS]->(cl:Class {{equipment: "True"}})<-[:REFERS_TO_CLASS]-(sch:Schedule)-[:REFERS_TO_GROUP]->(g:Group)<-[:STUDY_IN]-(s:Student) 
        WHERE sch.date >= {start_date} AND sch.date <= {end_date}
        WITH cl.title as class_title, sch.date as date ,sch.pair_number AS pair_number, count(DISTINCT s) AS student_count
        RETURN class_title, date, pair_number, student_count"""
    result = neo4j_graph.run(query)

    info = [[], [], [], []]
    for record in result:
        date_change = int(record["date"])*24*60*60
        dt = datetime.fromtimestamp(date_change)
        dt = dt.strftime('%Y-%m-%d')
        info[0].append(record["class_title"])
        info[1].append(str(dt))
        info[2].append(record["pair_number"])
        info[3].append(record["student_count"])
    return info




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12000)

