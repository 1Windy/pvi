from settings import db
import enum


class StatusEnum(enum.Enum):
    Preparing = 'Preparing'
    OnGoing = 'Ongoing'
    Finished = 'Finished'

    @classmethod
    def details(cls):
        return [i.value for i in cls]


class BHA(db.Model):
    __tablename__ = 'BHA'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100))
    case_file = db.Column(db.String(256))
    description = db.Column(db.String(512))
    create_by = db.Column(db.String(20))
    date = db.Column(db.String(20))
    survey_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default=StatusEnum.Preparing.value)
    component = db.relationship('BHA_Component', backref='bha')


class BHA_Component(db.Model):
    __tablename__ = 'BHA_Component'
    id = db.Column(db.Integer, primary_key=True)
    bha_id = db.Column(db.Integer, db.ForeignKey('BHA.id', ondelete='CASCADE', onupdate='CASCADE'))
    bha_type = db.Column(db.String(20))
    bit_size = db.Column(db.String(20))

    def __repr__(self):
        return '<bha_type: %s bha_id: %s>' % (self.bha_type, self.bha_id)
