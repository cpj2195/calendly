from pynamodb.models import Model


class PynamoBaseModel(Model):
    """
    Base Model for pynamo models.
    Conatins base functions for all models such as a serializer.
    """
    def to_dict(self):
        """
        Serializes the Pynamo model to a dict

        Parameters
        ----------
        self: Reference object for the class object

        Returns
        -------
        serialized_response: dict
            Serialized dictionary
        """
        serialized_response = {}
        for key in self.attribute_values:
            serialized_response[key] = self.__getattribute__(key)
        return serialized_response
