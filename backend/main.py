from flask import Flask, jsonify, request

from .entities.entity import Session, engine, Base
from .entities.servers import Server, ServerSchema

# creating the Flask application
app = Flask(__name__)

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/servers')
def get_servers():
    # fetching from the database
    session = Session()
    servers_objects = session.query(Server).all()

    # transforming into JSON-serializable objects
    schema = ServerSchema(many=True)
    all_servers = schema.dump(servers_objects)

    # serializing as JSON
    session.close()
    return jsonify(all_servers.data)


@app.route('/servers', methods=['POST'])
def add_exam():
    # mount exam object
    posted_server = ServerSchema(only=('serverID', 'serverName', 'serverAddress'))\
        .load(request.get_json())

    server = Server(**posted_server.data, created_by="HTTP post request")

    # persist exam
    session = Session()
    session.add(server)
    session.commit()

    # return created exam
    new_server = ServerSchema.dump(server).data
    session.close()
    return jsonify(new_server), 201