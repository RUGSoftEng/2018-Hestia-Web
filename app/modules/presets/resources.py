"""
Defines the endpoints allowing for access and manipulation of servers.
A server represents a remote Hestia controller.
"""

from flask_restplus import (
    Resource,
    Namespace,
    fields,
)
from sqlalchemy.orm import (exc) # TODO there may be a more elegant way to manage this
from app.extensions import (DB)
from app.modules.util import (route_request)
from app.extensions.auth.authentication import (
    requires_auth,
    get_user_id,
)
from ..servers.models import (ServerModel)
from .schemas import (PresetSchema)
from .models import (PresetModel)


NAMESPACE = Namespace('servers', "The central point for all your server (controller) needs.")

PAYLOAD = NAMESPACE.model('payload', {
    'preset_name': fields.String(
        readOnly=True,
        description='The type of request to make to the server'
    ),
})



@NAMESPACE.route('/<string:server_id>/presets/')
@NAMESPACE.param('server_id', 'The server identifier')
class Presets(Resource):

    """ GET all presets in given server, POST a new preset. """
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id):
        """
        List of presets.
        Returns a list of presets starting from ``offset`` limited by ``limit``
        parameter.
        """
        try:
            DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        presets = DB.session.query(PresetModel).filter_by(server_id = server_id,)
        schema = PresetSchema(many=True)
        all_presets = schema.dump(presets).data
        return all_presets

    @NAMESPACE.expect(PAYLOAD)
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
       payload = NAMESPACE.apis[0].payload
       try:
           DB.session.query(ServerModel).filter_by(
               server_id=server_id, user_id=get_user_id()).one()
       except exc.NoResultFound:
           return "", 404

       payload["server_id"] = server_id
       posted_preset = PresetSchema(only=(
               'preset_name',
               'server_id',
           )).load(payload)
       preset = PresetModel(**posted_preset.data)

       DB.session.begin()
       DB.session.add(preset)
       DB.session.commit()

       return PresetSchema().dump(preset).data

@NAMESPACE.route('/<string:server_id>/presets/<string:preset_id>')
@NAMESPACE.param('server_id', 'The server identifier')
class Preset(Resource):

    """ GET all presets in given server, POST a new preset. """
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id, preset_id):
        """
        List of presets.
        Returns a list of presets starting from ``offset`` limited by ``limit``
        parameter.
        """
        try:
            DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        try:
            preset = DB.session.query(PresetModel).filter_by(
                server_id = server_id,
                preset_id=preset_id
            ).one()
        except exc.NoResultFound:
            return "", 404

        return PresetSchema().dump(preset).data


    @NAMESPACE.doc(security='apikey')
    def delete(self, server_id, preset_id):
        """
        List of presets.
        Returns a list of presets starting from ``offset`` limited by ``limit``
        parameter.
        """
        try:
            DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        try:
            preset = DB.session.query(PresetModel).filter_by(
                server_id = server_id,
                preset_id=preset_id
            ).one()
        except exc.NoResultFound:
            return "", 404

        DB.session.begin()
        DB.session.delete(preset)
        DB.session.commit()

        return "", 204
