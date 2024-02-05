import requests

def query_blazegraph(sparql_query):
    blazegraph_endpoint = 'http://localhost:9999/bigdata/sparql'  # Replace with your Blazegraph SPARQL endpoint URL
    headers = {'Accept': 'application/json'}  # Specify the desired result format

    params = {
        'query': sparql_query,
        'format': 'json'  # Specify the desired result format
    }

    response = requests.get(blazegraph_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        results = response.json()
        return results
    else:
        print(f"Failed to execute SPARQL query. Status code: {response.status_code}")
        return None


def build_query(selected_origins, selected_topics):
    if(selected_origins):
        selected_origins_string = ''
        for origin in selected_origins:
            if(origin != selected_origins[-1]):
                selected_origins_string += '\"' + origin + '\", ' 
            else:
                selected_origins_string += '\"' + origin + '\"' 
        selected_origins_string = '(' + selected_origins_string + ')'

    if(selected_topics):
        selected_topics_string = ''
        for topic in selected_topics:
            if(topic != selected_topics[-1]):
                selected_topics_string += '\"' + topic + '\", ' 
            else:
                selected_topics_string += '\"' + topic + '\"' 
        selected_topics_string = '(' + selected_topics_string + ')'

    
        sparql_query = """
        PREFIX ns: <http://wade-project.org/news#>

        SELECT ?predicate ?object
        WHERE {{
        GRAPH ?graph {{
            ?subject ns:origin ?origin ;
             ns:topic ?topic .
            FILTER (?origin IN {origins} && ?topic IN {topics})
            ?subject ?predicate ?object .
        }}
        }}
        """.format(origins = selected_origins_string, topics = selected_topics_string)

        return sparql_query



def query_by_origins(selected_origins, selected_topics):
    query = build_query(selected_origins, selected_topics)

    result = query_blazegraph(query)

    i = 0;
    dict = {}
    final_result = {"items": []}
    for r in result["results"]["bindings"]:
            predicate = r['predicate']['value'].split('#')[1]
            obj = r['object']['value']
            if(i < 4):
                dict.update({predicate: obj})
            else:
                i=0
                dict.update({predicate: obj})
                final_result['items'].append(dict)
                dict = {}
            i+=1
    return final_result


        
