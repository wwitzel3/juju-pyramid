
from charmhelpers.core.charmframework.helpers import Relation

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


class PostgreSQLRelation(Relation):
    """
    Relation subclass for handling relations using the ``postgresql`` interface protocol.

    As mentioned in :class:`Relation`, all variables (including `dsn_format`) can be
    overridden when instantiating the class.
    """
    relation_name = 'db'
    required_keys = ['host', 'user', 'password', 'database']
    dsn_format = 'postgresql://{user}:{password}@{host}/{database}'
    """
    In addition to the :attr:`required_keys`, a ``dsn`` value is constructed, based
    on this format string, and added to the :meth:`filtered_data`.
    """

    def filtered_data(self, remote_service=None):
        """
        Get the filtered data, as per :meth:`Relation.filtered_data`, and add
        a ``dsn`` entry constructed from the other values.
        """
        data = super(PostgreSQLRelation, self).filtered_data(remote_service)
        for unit_name, unit_data in data.items():
            unit_data['dsn'] = self.dsn_format.format(**unit_data)
        return data


class RedisRelation(Relation):
    """
    Relation subclass for handling relations using the ``redis`` interface protocol.

    As mentioned in :class:`Relation`, all variables (including `dsn_format`) can be
    overridden when instantiating the class.
    """
    relation_name = 'db'
    required_keys = ['hostname', 'port']
    dsn_format = 'redis://{hostname:port}/0'
    """
    In addition to the :attr:`required_keys`, a ``dsn`` value is constructed, based
    on this format string, and added to the :meth:`filtered_data`.
    """

    def filtered_data(self, remote_service=None):
        """
        Get the filtered data, as per :meth:`Relation.filtered_data`, and add
        a ``dsn`` entry constructed from the other values.
        """
        data = super(RedisRelation, self).filtered_data(remote_service)
        for unit_name, unit_data in data.items():
            unit_data['dsn'] = self.dsn_format.format(**unit_data)
        return data

