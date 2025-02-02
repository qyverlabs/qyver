Module qyver.framework.dsl.storage.vector_database
========================================================

Classes
-------

`VectorDatabase()`
:   Abstract base class for a Vector Database.
    
    This class serves as a blueprint for vector databases, ensuring that any concrete implementation
    provides a connector to the vector database.
    
    Attributes:
        _vdb_connector (VDBConnectorT): An abstract property that should return an instance of a VDBConnector.

    ### Ancestors (in MRO)

    * abc.ABC
    * typing.Generic

    ### Descendants

    * qyver.framework.dsl.storage.in_memory_vector_database.InMemoryVectorDatabase
    * qyver.framework.dsl.storage.mongo_db_vector_database.MongoDBVectorDatabase
    * qyver.framework.dsl.storage.qdrant_vector_database.QdrantVectorDatabase
    * qyver.framework.dsl.storage.redis_vector_database.RedisVectorDatabase
