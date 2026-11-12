from db import conn
from flask import request,jsonify,Blueprint
import sqlite3

tasks_bp = Blueprint("tasks",__name__)

@tasks_bp.route('/tasks',methods=['GET'])
def get_tasks():
    cursor = conn.cursor()
    cursor.execute("select * from tasks")
    tasks_list=[dict(row) for row in cursor.fetchall()]
    if not tasks_list:
        return jsonify({"mes":"当前还没有任务,请新建","data":[]})
    else:
        return jsonify({"mes":"获取任务列表成功","data":tasks_list})
@tasks_bp.route('/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
   cursor = conn.cursor()
   row = cursor.execute("select * from tasks where id =?",(task_id,)).fetchone()
   if row is None:
       return jsonify({"mes":"没有你要找的任务","data":[]}),404
   return jsonify({"mes":"ok","data":dict(row)}),200

@tasks_bp.route('/tasks',methods=['POST'])
def post_task():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"mes":"title不能为空","data":[]}),400
    cursor = conn.cursor()
    try:
        cursor.execute("insert into tasks (title) values(?)",(title,))
        conn.commit()
        if cursor.rowcount == 1:
            cursor.execute("select * from tasks where id =?",(cursor.lastrowid,))
            row = cursor.fetchone()
            return jsonify(dict(row)),201
    except sqlite3.IntegrityError as e:
        print("约束错误：", e)
    except sqlite3.OperationalError as e:
        print("SQL 错误：", e)
    return jsonify({"mes":"新增失败","data":[]}),500

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    data = request.get_json()
    title = data.get("title")
    done = data.get("done",0)
    if not title:
        return jsonify({"mes":"title不能为空","data":[]}),400
    cursor = conn.cursor()
    try:
        cursor.execute("update tasks set title =?, done = ? where id =?",(title,done,task_id))
        if cursor.rowcount:
            conn.commit()
            return jsonify({"mes": "修改成功","data":[]}),200
    except sqlite3.IntegrityError as e:
        print("约束错误：", e)
    except sqlite3.OperationalError as e:
        print("SQL 错误：", e)
    except sqlite3.ProgrammingError as e:
        print("执行失败",e)
    return jsonify({"mes":"修改失败"}),500

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor = conn.cursor()
    try:
        cursor.execute("delete from tasks where id = ?",(task_id,))
        if cursor.rowcount:
            conn.commit()
            return jsonify({"mes":"删除成功","data":[]}),200
    except sqlite3.IntegrityError as e:
        print("约束错误：", e)
    except sqlite3.OperationalError as e:
        print("SQL 错误：", e)
    except sqlite3.ProgrammingError as e:
        print("执行失败",e)
    return jsonify({"mes":"删除失败","data":[]}),500