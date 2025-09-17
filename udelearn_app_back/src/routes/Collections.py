from flask import Blueprint,jsonify,request
#Entities
from models.entities.Collection import Collection
import json
import traceback

#Models
from models.CollectionModel import CollectionModel

main = Blueprint('collections_blueprint',__name__)

@main.route('/')
def get_collections():
    try:
        collections=CollectionModel.get_collections()
        return jsonify(collections)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@main.route('/<id>')
def get_collection(id):
    try:
        collection = CollectionModel.get_collection(id)
        if collection != None:
            return jsonify(collection)
        else:
            return jsonify({}),404
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
# @main.route('/add', methods=['POST'])
# def add_collection():
#     try:
#         # Get the raw JSON
#         data = request.get_json()
#         print("Received JSON:", data)  # Debug the incoming JSON
        
#         # Validations
#         if not isinstance(data, dict):
#             return jsonify({'message': 'Invalid JSON format'}), 400
        
#         title = data.get('title')
#         description = data.get('description')
#         document = data.get('document')
        
#         if not title or not description or not document:
#             return jsonify({'message': 'Missing required fields'}), 400
            
#         print("Parsed fields:", {'title': title, 'description': description, 'document': document})  # Debug parsed fields
        
#         collection = Collection(
#             title=title,
#             description=description,
#             document=document
#         )
#         print("Collection object:", {
#             'title': collection.title,
#             'description': collection.description,
#             'document': collection.document
#         })  # Debug Collection object
        
#         affected_rows = CollectionModel.add_collection(collection)
#         if affected_rows == 1:
#             return jsonify(collection.id)
#         else:
#             return jsonify({'message': "Error on insert"}), 500
#     except Exception as ex:
#         return jsonify({'message': str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_collection():
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        file = request.files.get("file")

        if not title or not description or not file:
            return jsonify({'message': 'Missing required fields'}), 400

        if not file.filename.endswith(".json"):
            return jsonify({'message': 'Invalid file type, must be .json'}), 400

        # Read the uploaded JSON file
        file_content = file.read().decode("utf-8")
        document = json.loads(file_content)

        collection = Collection(
            title=title,
            description=description,
            document=document
        )

        affected_rows = CollectionModel.add_collection(collection)
        if affected_rows == 1:
            return jsonify({"id": collection.id})
        else:
            return jsonify({'message': "Error on insert"}), 500

    except Exception as ex:
        traceback.print_exc()
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<id>', methods=['DELETE'])
def delete_collection(id):
    try:

        collection = Collection(id)

        affected_rows=CollectionModel.delete_collection(collection)
        if affected_rows == 1:
            return jsonify(collection.id)
        else:
            return jsonify({'message': "No collection deleted"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/update/<id>', methods=['PUT'])
def update_collection(id):
    try:
        # Get the raw JSON
        data = request.get_json()
        print("Received JSON:", data)  # Debug the incoming JSON
        
        # Validations
        if not isinstance(data, dict):
            return jsonify({'message': 'Invalid JSON format'}), 400
        
        #id = data.get('id')
        title = data.get('title')
        description = data.get('description')
        document = data.get('document')
        
        if not title or not description or not document:
            return jsonify({'message': 'Missing required fields'}), 400
        
        collection = Collection(
            id = id,
            title=title,
            description=description,
            document=document
        )
        
        affected_rows = CollectionModel.update_collection(collection)
        if affected_rows == 1:
            return jsonify(collection.id)
        else:
            return jsonify({'message': "No collection updated"}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    