"""
Defines the endpoints allowing for access and manipulation of presets
associated with a particular Hestia controller.
"""

from flask_restplus import (
    Resource,
    Namespace,
    fields,
)
from sqlalchemy.orm import (exc)
from app.extensions import (DB)
from app.modules.util import (route_request)
from app.extensions.auth.authentication import (
    requires_auth,
    get_user_id,
)
from ..servers.models import (ServerModel)
from ..servers.schemas import (ServerSchema)
from .schemas import (PresetSchema)
from .models import (PresetModel)

NAMESPACE = Namespace(
    'servers', "The central point for all your server (controller) needs.")

PRESET_PAYLOAD = NAMESPACE.model('payload', {
    'preset_name': fields.String(
        readOnly=True,
        description='The name of a preset.'
    ),
})


@NAMESPACE.route('/<string:server_id>/presets/')
@NAMESPACE.param('server_id', 'The server identifier')
class Presets(Resource):

    """ GET all presets in given server, POST a new preset. """
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id):
        """
        List of presets. Returns a list of all presets associated with a
        server. If the server is not associated with the user it returns an
        exception.
        """
        try:
            DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        presets = DB.session.query(PresetModel).filter_by(server_id=server_id,)
        schema = PresetSchema(many=True)
        all_presets = schema.dump(presets).data
        return all_presets

    @NAMESPACE.expect(PRESET_PAYLOAD)
    @requires_auth
    @NAMESPACE.doc(security='apikey')
    def post(self, server_id):
        """
        Post a preset to a server.
        """
        payload = NAMESPACE.apis[0].payload
        try:
            server_object = DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        # transforming into JSON-serializable objects
        server = ServerSchema().dump(server_object).data

        payload["server_id"] = server_id

        server_address = server['server_address'] + \
            ':' + server['server_port'] + '/devices/'

        # Get the current state of the server.
        payload["preset_state"] = str(
            route_request("GET", server_address, "").json)

        posted_preset = PresetSchema(only=(
            'preset_name',
            'preset_state',
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

    """ GET a particular preset in given server, DELETE a preset. """
    @NAMESPACE.doc(security='apikey')
    def get(self, server_id, preset_id):
        """
        Return a specific preset with ``preset_id`` associated with a server with ``server_id``
        """
        try:
            DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        try:
            preset = DB.session.query(PresetModel).filter_by(
                server_id=server_id,
                preset_id=preset_id
            ).one()
        except exc.NoResultFound:
            return "", 404

        return PresetSchema().dump(preset).data

    @NAMESPACE.doc(security='apikey')
    def delete(self, server_id, preset_id):
        """
        Delete a specific preset with ``preset_id`` associated with a server with ``server_id``
        """
        try:
            DB.session.query(ServerModel).filter_by(
                server_id=server_id, user_id=get_user_id()).one()
        except exc.NoResultFound:
            return "", 404

        try:
            preset = DB.session.query(PresetModel).filter_by(
                server_id=server_id,
                preset_id=preset_id
            ).one()
        except exc.NoResultFound:
            return "", 404

        DB.session.begin()
        DB.session.delete(preset)
        DB.session.commit()

        return "", 204
