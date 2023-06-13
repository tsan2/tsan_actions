# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# DB_NAME=os.environ.get('DB_NAME')
# DB_USER=os.environ.get('DB_USER')
# DB_PASSWORD=os.environ.get('DB_PASSWORD')
# DB_HOST=os.environ.get('DB_HOST')
# DB_PORT=os.environ.get('DB_PORT')

import os
os.environ ["DB_NAME"] = 'tsan_actions'
os.environ ["DB_USER"] = 'postgres'
os.environ ["DB_PASSWORD"] = 'Nasta678!'
os.environ ["DB_HOST"] = 'localhost'
os.environ ["DB_PORT"] = '5432'

DB_NAME=os.environ['DB_NAME']
DB_USER=os.environ['DB_USER']
DB_PASSWORD=os.environ['DB_PASSWORD']
DB_HOST=os.environ['DB_HOST']
DB_PORT=os.environ['DB_PORT']
