import json
import os

import xmltodict

from manage import app
from models.bha import BHA, BHAComponent, RoundEnum, BHARound
from settings import db

case_file_dir = os.path.abspath(os.pardir) + '/Casefile'
sqlite_dir = 'sqlite:///' + os.path.join(os.path.abspath(os.pardir) + '/', 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_dir


def file_name(file_dir):
    for files in os.walk(file_dir):
        return files


def xml_to_json(file):
    with open(file, 'r') as f:
        xml_str = f.read()
    xml_parse = xmltodict.parse(xml_str)
    json_str = json.dumps(xml_parse, indent=1)
    update_json = json_str.replace("@", "")
    data = json.loads(update_json)
    return data


def import_db():
    files = file_name(case_file_dir)
    for file in files[2]:
        data = xml_to_json(case_file_dir + '/' + file)
        with app.app_context():
            bha = BHA(project=data['BHAData']['ProductName'], case_file=file,
                      description=data['BHAData']['General']['Comments'].replace(' ', ''),
                      create_by=data['BHAData']['General']['By'], date=data['BHAData']['General']['Date'],
                      survey_type=data['BHAData']['General']['SurveyType'])
            for i in RoundEnum.details():
                bha_round = BHARound(round=i, bha=bha)
                db.session.add(bha_round)
                db.session.commit()
            for row in data['BHAData']['BHA']['BHA']['BHAComponentRow']:
                if row['Type'] == 'Bit':
                    component = BHAComponent(bha_type=row['Type'], bit_size=row['BHAComponet']['Size'], bha=bha)
                    db.session.add(component)
                    db.session.commit()
                else:
                    component = BHAComponent(bha_type=row['Type'], bha=bha)
                    db.session.add(component)
                    db.session.commit()
    return 'success'


if __name__ == '__main__':
    print(import_db())
