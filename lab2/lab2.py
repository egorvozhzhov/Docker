from py2neo import Graph, NodeMatcher
from neo4j import GraphDatabase
import redis





def start_lab2(course_title, date1, date2):
    pair2, number2, groups2, day2 = var2(course_title, date1, date2)
    res5= get_info(groups2)
    final = []

    for i in range(len(pair2)):
        final.append([pair2[i], day2[i], number2[i], res5[i]])
    return final

def var2(title, date1, date2):
    graph = Graph("bolt://neo4j:7687")
    uri = "bolt://neo4j:7687"
    data2 = []
    groups2 = []
    pair2 = []
    day2= []
   
    query = (
        "MATCH (c:Course {title: $title_course})-[:HAS_CLASS]->(cl:Class {equipment: 'True'})<-[:REFERS_TO_CLASS]-(sch:Scheldue)-[:REFERS_TO_GROUP]->(g:Group) WHERE sch.date >= date($Date1) AND sch.date <= date($Date2) WITH cl, sch.date AS day, sch.pair_number AS pair, COLLECT(g.id) AS groups "
        "RETURN cl.title AS lecture_title, pair, day, groups"
    )

    with GraphDatabase.driver(uri) as driver:
        with driver.session() as session:
            result = session.run(query, title_course = title, Date1 = date1, Date2= date2)
            for record in result:
                data2.append(record["lecture_title"])
                pair2.append(record["pair"])
                groups2.append(record["groups"])
                day2.append(record["day"])
                
    return data2, pair2, groups2, day2


def get_info(groups):
    r = redis.Redis(
        host='redis',
        port=6379,
        decode_responses=True
    )
    res = []
    for group in groups:
        count = 0;
        for i in range(len(group)):
            group_key = f"group:{group[i]}:*"
            group_keys = r.keys(group_key)
            for key in group_keys:
                count += r.scard(key)
        res.append(count)
            
    return res


