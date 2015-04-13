
from charmhelpers.core.charmframework import Relation

class MongoDBRelation(Relation):
    """
    Relation subclass for handling relations using the ``mongodb`` interface protocol.
    """
   
    relation_name = "mongodb"
    required_keys = ["hostname", "port"]
    url = "{hostname}:{port}"

    def filtered_data(self, remote_service=None):
        """
        Get the filtered data, interpolating the derived ``url`` value from the
        ``host`` and ``port`` values provided by mongodb.
        """
        data = super(MongoDBRelation, self).filtered_data(remote_service)
        for unit_name, unit_data in data:
            unit_data['url'] = self.url.format(**unit_data)

