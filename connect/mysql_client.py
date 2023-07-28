from functools import wraps

import mysql.connector


def _reconnect(func):
    @wraps(func)
    def rec(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except (mysql.connector.Error, mysql.connector.Warning):
            self.connect()
            result = func(self, *args, **kwargs)
            return result

    return rec


class MysqlClient:
    def __init__(self, host, port, user, password):
        self.cnx = mysql.connector.connect(
            host=host,  # 数据库主机地址
            port=port,  # 端口号
            database="cicd",  # 数据库
            user=user,  # 数据库用户名
            passwd=password,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.cnx.cursor()

    @_reconnect
    def find_project_by_name(self, value):
        project_query = ("SELECT id, project_id, project_name, ci_ref, project_gitlab_name "
                         "FROM gitlab_project where suggest_name like %s")
        select_values = ('%' + value + '%',)
        self.cursor.execute(project_query, select_values)
        res = self.cursor.fetchall()
        self.cnx.commit()
        return res

    @_reconnect
    def find_project_by_project_id(self, value):
        project_query = ("SELECT id, project_id, project_name, ci_ref, project_gitlab_name, ci_user_id "
                         "FROM gitlab_project where project_id = %s")
        select_values = (value,)
        self.cursor.execute(project_query, select_values)
        res = self.cursor.fetchall()
        self.cnx.commit()
        if len(res) > 0:
            return res[0]
        else:
            return None

    @_reconnect
    def find_at_user(self, value):
        project_query = "SELECT ci_user_id FROM gitlab_project where project_id = %s"
        select_values = (value,)
        self.cursor.execute(project_query, select_values)
        res = self.cursor.fetchall()
        self.cnx.commit()
        if len(res) > 0:
            return res[0][0]
        else:
            return None

    @_reconnect
    def update_project_ci(self, values):
        project_query = "update gitlab_project set ci_user_id = %s,ci_user_nickname = %s, " \
                        "ci_ref = %s where project_id = %s"
        update_values = values
        self.cursor.execute(project_query, update_values)
        self.cnx.commit()

    @_reconnect
    def find_rollback_ref(self, value):
        project_query = "SELECT ci_ref FROM project_ci_log where project_id = %s order by update_time DESC limit 2"
        select_values = (value,)
        self.cursor.execute(project_query, select_values)
        res = self.cursor.fetchall()
        self.cnx.commit()
        return res

    @_reconnect
    def save_project_ci(self, values):
        project_query = "insert into project_ci_log (project_id, ci_type,ci_ref,ci_user_nickname) values " \
                        "(%s,%s,%s,%s)"
        self.cursor.execute(project_query, values)
        self.cnx.commit()
