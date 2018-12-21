from flask import (
    request, render_template, views, Blueprint, flash, jsonify
)
from flask_paginate import Pagination
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from bha.forms import UpdateStatusFrom
from models import BHAComponent, BHA, StatusEnum, BHARound, RoundEnum
from settings import db, SQLALCHEMY_DATABASE_URI
from utils.paginate import get_page

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}, poolclass=StaticPool)
session = sessionmaker(engine)()

bp = Blueprint('bha', __name__)


class BHAView(views.MethodView):

    def get(self):
        query = []
        for k, v in request.args.items():
            query.append(BHA.project == v) if k == 'project' and v else None
            query.append(BHA.survey_type == v) if k == 'survey_type' and v else None
            query.append(BHA.case_file == v) if k == 'case_file' and v else None
            query.append(BHA.create_by == v) if k == 'create_by' and v else None
            query.append(BHAComponent.bha_type == v) if k == 'bha_type' and v else None
            query.append(BHAComponent.bit_size == v) if k == 'bit_size' and v else None

        _round = request.args.get('round', 'alpha')
        _status = request.args.get('bha_status', StatusEnum.Preparing.value)

        if request.args.get('bha_type') or request.args.get('bha_size'):
            bha_ids = session.query(BHA.id).join(BHAComponent).filter(*query).subquery()
        else:
            bha_ids = session.query(BHA.id).filter(*query).subquery()

        bha_round_set = session.query(BHARound).filter(
            BHARound.bha_id.in_(bha_ids),
            BHARound.round == _round,
            BHARound.status == _status
        )

        page, start, end = get_page()
        rounds = bha_round_set.slice(start, end)
        total = bha_round_set.count()
        pagination = Pagination(bs_version=3, page=page, total=total, outer_window=1, inner_window=3)

        context = {
            "round": _round,
            "bha_rounds": rounds.all(),
            "pagination": pagination,
            "bha_status": _status,
            "statuses": StatusEnum.details(),
            "rounds": RoundEnum.details()
        }

        return render_template('bha.html', **context)

    def post(self):
        form = UpdateStatusFrom(request.form)
        if not form.validate():
            flash('param error: {}'.format(form.get_error()))
            return jsonify({'code': 400, 'message': form.get_error()})

        id = form.id.data
        _round = form.round.data
        status = form.status.data
        bha_round = BHARound.query.get_or_404(id)
        bha_round.round = _round
        bha_round.status = status
        db.session.commit()
        return jsonify({'code': 200, 'message': 'update success', 'status': status})


bp.add_url_rule('/', view_func=BHAView.as_view('bha'))
