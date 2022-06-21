import pandas as pd
import sqlite3
import os

path = os.path.realpath(__file__).rstrip("ELISA_core\static\python\database.py")+"db.sqlite3"
#C:\Users\Mila\PycharmProjects\BPEXI\ELISA_app\ELISA_core\static\python\database.py
#C:\Users\Mila\PycharmProjects\BPEXI\ELISA_app\db.sqlite3

plates = pd.DataFrame(columns=['ID', 'Name', 'Data'])
cxn = sqlite3.connect(path)
cxn.cursor().executescript('drop table if exists plates')
plates.to_sql('plates', cxn, index=False)
cxn.close()

# python manage.py inspectdb plates > ELISA_app\models.py