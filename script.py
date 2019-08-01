#!/usr/bin/env python
# coding: utf-8

import json
import time
from io import BytesIO
from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2

conn = psycopg2.connect(user='postgres',            # connect to postgres database  
                        password='11311131',
                        dbname='git_test',
                       )
                        #host='server',             # use for reomote postgres server
                        #port='5432')
table = 'test_git6'                                 # table name 
local_host = 'localhost'                            # ip/port local server listener  (should be opened for internet connection )
local_port = 8080

def main():
    httpd = HTTPServer((local_host, local_port), SimpleHTTPRequestHandler)
    httpd.serve_forever()
    
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler): 

    def do_GET(self):               
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Pong!')

    def do_POST(self):                              
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)                     # http status code
        self.end_headers()
        response = BytesIO()
        response.write(b'POST request recived')
        self.wfile.write(response.getvalue())
        
        data = json.loads(body.decode('utf-8'))
        git_event = self.headers['x-github-event']  # http packet parsing 
        uuid = self.headers['X-GitHub-Delivery']
        output = insert_body(data, git_event, uuid)
        
        if output != None:                          # cheker request (NOT create,delete,push,pull request headers)
            cur = conn.cursor()
            cur.execute(output)
            conn.commit()
            cur.close()
            print('ok')
        else:
            print('operation aborted!')
            
def insert_body (data, git_event, uuid):              #forming a request to the database
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    if git_event == 'create' or git_event == 'delete':
        ref=data['ref']
        insert = """INSERT INTO %s(          
                    ref, git_event,
                    uuid, timestamp
                    )
                    VALUES(
                        '%s', '%s',
                        '%s', '%s');
                    """ % (
                        table,
                        ref, git_event,
                        uuid, ts)                      #request body

    elif git_event == 'push':
        ref=data['ref']
        commit_id = data['commits'][0]['id']
        tree_id = data['commits'][0]['tree_id']
        insert = """ INSERT INTO %s(
                    ref, git_event, uuid,
                    commit_id, tree_id, timestamp
                    )
                    VALUES(
                        '%s', '%s', '%s',
                        '%s', '%s', '%s');
                    """ % (
                        table,
                        ref, git_event, uuid,
                        commit_id, tree_id, ts)

    elif git_event == 'pull_request':
        ref = data['pull_request']['head']['ref']
        commit_id = data['pull_request']['id']
        commits_url = data['pull_request']['commits_url']
        insert = """INSERT INTO %s(
                         ref, git_event, uuid,
                         timestamp, commits_url
                    )
                    VALUES(
                        '%s', '%s', '%s',
                        '%s', '%s');
                    """ % ( 
                        table,
                        ref, git_event, uuid, 
                        ts, commits_url)
    else:
        insert = None 
    return insert
    
if __name__ == '__main__':
    main()            

