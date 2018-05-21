"""
Defines the endpoints allowing for access and manipulation of users.
"""

from flask_restplus import (
    Resource,
    Namespace,
)

from app.extensions import (DB)

NAMESPACE = Namespace('users', "Manipulate users of the system.")

def get_user_id():
    return "1"

def commit_or_abort(session, default_error_message="The operation failed to complete"):
        """
        Simplifies creating database sessions.
        """
        try:
            with session.begin():
                yield
        except ValueError as exception:
            # log.info("Database transaction was rolled back due to: %r", exception)
            print("ValueError")
            http_exceptions.abort(code=HTTPStatus.CONFLICT, message=str(exception))
        except sqlalchemy.exc.IntegrityError as exception:
            print("SQLAlchemy Error")
            # log.info("Database transaction was rolled back due to: %r", exception)
            http_exceptions.abort(
                code=HTTPStatus.CONFLICT,
                message=default_error_message
            )

@NAMESPACE.route('/')
class Users(Resource):
    """ POST a new user. """
    def post(self):
        """
        List of users.
        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        user_id = {
            'user_id': get_user_id()
        }
        new_user = "test"
        DB.session.begin()
        # DB.session.add(new_user)

        return new_user
