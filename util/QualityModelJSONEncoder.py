import json

from domain.model.QualityModel import QualityModel


class QualityModelJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QualityModel):
            return obj.serialize()
        return json.JSONEncoder.default(self, obj)