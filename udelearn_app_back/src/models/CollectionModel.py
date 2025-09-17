from database.db import get_connection
from .entities.Collection import Collection
from psycopg2.extras import Json 
from psycopg2 import errors
import simplejson
import traceback
from psycopg2.errors import UniqueViolation
#To raise uniqueness error
UniqueViolation = errors.lookup('23505')

class CollectionModel():

    @classmethod
    def get_collections(cls):
        try:
            connection=get_connection()
            collections = []

            with connection.cursor() as cursor:
                cursor.execute('SELECT id,title,description,document FROM "collections" ORDER BY id ASC;')
                #cursor.execute('SELECT * FROM collections')
                resultset = cursor.fetchall()

                for row in resultset:
                    collection=Collection(row[0],row[1],row[2],row[3])
                    collections.append(collection.to_JSON())
                
            connection.close()
            return collections
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_collection(cls,id):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                
                cursor.execute('SELECT id,title,description,document FROM "collections" WHERE id = %s',(id,))
                #cursor.execute('SELECT * FROM collections')
                row = cursor.fetchone()
                collection=None
                if row != None:
                    collection = Collection(row[0],row[1],row[2],row[3])
                    collection = collection.to_JSON()
                
            connection.close()
            return collection
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_collection(cls,collection):
        try:
            connection=get_connection()
            try:
                with connection.cursor() as cursor:
                    #print(f"Document: {collection.document}, Type: {type(collection.document)}")
                    #cursor.execute('INSERT into collections (title,description,document) VALUES (%s,%s,%s)',(collection.title,collection.description,psycopg2.extras.Json(collection.document)))
                    print("title: ",collection.title)
                    #print(type(collection.document))
                    print("description: ",collection.description)
                    print("document: ", collection.document)
                    cursor.execute('INSERT INTO collections (title, description, document) VALUES (%s, %s, %s) RETURNING id',(collection.title, collection.description, Json(collection.document)))
                    affected_rows = cursor.rowcount
                    connection.commit()

                connection.close()
                return affected_rows
            except UniqueViolation as err:
                traceback.print_exc()
                connection.rollback()
        except Exception as ex:
            traceback.print_exc()
            raise Exception(ex)
        
    @classmethod
    def delete_collection(cls,collection):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('DELETE from collections WHERE id = %s',(collection.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_collection(cls,collection):
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                print("title: ",collection.title)
                print("description: ",collection.description)
                print("document: ", collection.document)
                cursor.execute('UPDATE collections SET title = %s, description = %s, document = %s WHERE id = %s',(collection.title, collection.description, Json(collection.document),collection.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
    
