#!/usr/bin/env python
# coding: utf-8

# In[2]:


import psycopg2
import time
conn = psycopg2.connect(user='postgres',
                        password='11311131',
                        dbname='git_test')

if __name__ == '__main__':
    cur = conn.cursor()
    cur.execute("""CREATE TABLE test_git6 (
                    id serial PRIMARY KEY,git_event text,
                    UUID uuid, ref text, tree_id text,
                    commit_id text, commits_url text ,
                    timestamp timestamp );""")
    conn.commit()
    cur.close()
    conn.close()

