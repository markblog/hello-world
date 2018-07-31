#!/usr/bin/env python
import inspect
import os
import random
import threading
import time
import random
from pyecharts import Scatter3D
from flask import Flask, render_template
from flask import g, render_template
from flask_cors import CORS
from werkzeug.local import LocalProxy

from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell
# from app.utils.flask_monitors import BehaviorMonitorCommand, Monitor
from flask_sqlalchemy import get_debug_queries
from flask import jsonify, request


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
CORS(app)
# Monitor(app, db = db)


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
# manager.add_command('log_behavior', BehaviorMonitorCommand(db))
manager.add_command('runserver', Server(host='0.0.0.0', port=5001))


@app.after_request
def after_request(response):
    print(get_debug_queries())
    for query in get_debug_queries():
        if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
            app.logger.warn(('Context:{}\n SLOW QUERY:{} \n PARAMETERS:{} \n'
                             'Duration:{}\n').format(query.context, query.statement, query.parameters, query.duration))

    return response


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']



    return jsonify({'r': 0, 'rs': 'pppppppppppppppppppppppp'})


# class RegistrationForm(Form):
#     name = TextField('Username', [length(min=4, max=25)])
#     email = TextField('Email Address', [length(min=6, max=35)])
#     password = PasswordField('New Password', [
#         Required(), EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         # user = User(name=form.name.data, email=form.email.data,
#         #             password=form.password.data)
#         # db.session.add(user)
#         # db.session.commit()
#         return 'register successed!'
#     return render_template('register.html', form=form)


if __name__ == '__main__':
    # start_runner()
    manager.run()
