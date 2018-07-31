# from flask import g
# from app.ext import raw_db
# from app.sqls import user_sqls
# from app.db_models.user import User, Role
# from app.ext import db
# #import you package here
# import datetime

# def get_user_by_email():
#     """
#     query user data filter by email
#     """
#     user = User.query.filter_by(email = g.args.get('email').lower()).first()
#     return user

# def create_user():
#     """
#     update user data to the database
#     """
#     user = User.from_dict(g.args)
#     user.email = user.email.lower()
#     db.session.add(user)
#     db.session.commit()


# # example for how to use raw sql 
# def get_all_group():

#     groups = raw_db.query(user_sqls.get_all_group).to_dict()

#     return groups
