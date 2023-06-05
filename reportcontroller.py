import datetime
from flask import request, jsonify
from sqlalchemy import text
from sqlalchemy.dialects.mssql.information_schema import columns
from sqlalchemy.orm import class_mapper

from Entity import Report

from database import db


def save_report():
    reporter = request.headers.get('Authorization')
    reported_username = request.json['reported_username']  # 被点赞者的j_username
    report_info = request.json['report_info']
    itype = request.json['itype']
    current_time = datetime.datetime.now()
    sqlstr = "INSERT INTO report (reporter, reported_username, message, time, itype) VALUES (:reporter, :reported_username, :report_info, :current_time,:itype)"

    # sqlstr="INSERT INTO report (reporter,reported_username,message) VALUES (:reporter, :reported_username,:report_info)"

    insert_query = text(sqlstr)
    try:
        db.session.execute(insert_query,
                           {'reporter': reporter, 'reported_username': reported_username, 'report_info': report_info,
                            'current_time': current_time, 'itype': itype})
        db.session.commit()
        response = {'status': 'success', 'message': 'Reported successfully.'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    return jsonify(response)


def get_report():
    try:
        reports = Report.query.all()

        # 构建要返回的信息字典列表
        # reports_data = [serialize_report(report,id) for report in reports]
        reports_data = [serialize_report(report, id + 1) for id, report in enumerate(reports)]

        response = {'status': 'success', 'reports': reports_data}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    # querry=text("select * from report")
    # result = db.session.execute(querry)
    return jsonify(response)


def serialize_report(report, id):
    return {
        'id': id,
        'reporter': report.reporter,
        'reported_username': report.reported_username,
        'message': report.message,
        'time': report.time.date().strftime('%Y-%m-%d'),
        'itype': report.itype
    }
# def serialize_report(report):
#     # columns = [column.key for column in class_mapper(Report).columns]
#     # return {column: getattr(report, column) for column in columns}
#      columns = [column.key for column in report.__table__.columns]
#      return {column: getattr(report, column) for column in columns}
