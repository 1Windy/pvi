from models import BHA_Component, BHA, StatusEnum
from flask import (
    request, render_template, views, Blueprint, flash, jsonify
)
from flask_paginate import Pagination
from settings import db, SQLALCHEMY_DATABASE_URI
from bha.forms import UpdateStatusFrom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.paginate import get_page

engine = create_engine(SQLALCHEMY_DATABASE_URI)
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
            query.append(BHA_Component.bha_type == v) if k == 'bha_type' and v else None
            query.append(BHA_Component.bit_size == v) if k == 'bit_size' and v else None

        if request.args.get('bha_type') or request.args.get('bha_size'):
            bha_set = session.query(BHA).join(BHA_Component).filter(*query)
        else:
            bha_set = session.query(BHA).filter(*query)

        page, start, end = get_page()
        bhas = bha_set.slice(start, end)
        total = bha_set.count()
        pagination = Pagination(bs_version=3, page=page, total=total, outer_window=1, inner_window=3)

        context = {
            "bhas": bhas,
            "pagination": pagination,
            "statuses": StatusEnum.details()
        }

        return render_template('bha.html', **context)

    def post(self):
        form = UpdateStatusFrom(request.form)
        if not form.validate():
            flash('param error: {}'.format(form.get_error()))
            return jsonify({'code': 400, 'message': form.get_error()})

        id = form.id.data
        status = form.status.data
        bha = BHA.query.get_or_404(id)
        bha.status = status
        db.session.commit()
        return jsonify({'code': 200, 'message': 'update success', 'status': status})


bp.add_url_rule('/', view_func=BHAView.as_view('bha'))
