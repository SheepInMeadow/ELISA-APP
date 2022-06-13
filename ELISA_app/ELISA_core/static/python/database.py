import pandas as pd
import sqlite3

plates = pd.DataFrame(columns=['ID', 'Name', 'Data'])
path = 'C:\\USERS\\David\\PycharmProjects\\BPEXI\\ELISA_app\\'
cxn = sqlite3.connect(path + 'db.sqlite3')
cxn.cursor().executescript('drop table if exists plates')
plates.to_sql('plates', cxn, index=False)
cxn.close()

# python manage.py inspectdb plates > ELISA_app\models.py