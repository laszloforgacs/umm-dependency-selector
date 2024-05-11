from marshmallow import fields, ValidationError, post_load, Schema

from domain.model.Measure import MeasurementMethod, BaseMeasure, DerivedMeasure
from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact


class EnumField(fields.Field):
    def __init__(self, enum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum = enum

    def _serialize(self, value, attr, obj, **kwargs):
        return value.name if value else None

    def _deserialize(self, value, attr, data, **kwargs):
        if value in self.enum.__members__:
            return self.enum[value]
        else:
            raise ValidationError(f"Invalid value '{value}' for field '{attr}'.")


class BaseMeasureSchema(Schema):
    class_name = fields.Str()
    name = fields.Str()
    unit = fields.Str()
    scale = fields.Float()
    measurement_method = EnumField(MeasurementMethod)
    visitor = fields.Str()
    value = fields.Raw(allow_none=True)

    @post_load
    def make_base_measure(self, data, **kwargs):
        return BaseMeasure(**data)


class DerivedMeasureSchema(Schema):
    class_name = fields.Str()
    name = fields.Str()
    unit = fields.Str()
    scale = fields.Float()
    measurement_method = EnumField(MeasurementMethod)
    children = fields.Dict(keys=fields.Str(), values=fields.Nested(BaseMeasureSchema))
    normalize_visitor = fields.Str()
    aggregate_visitor = fields.Str()
    value = fields.Raw(allow_none=True)

    @post_load
    def make_derived_measure(self, data, **kwargs):
        # Assuming children are passed as dictionary {key: base_measure_instance}
        return DerivedMeasure(**data)


class MeasureField(fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        measures = []
        for item in value:
            if 'base_measures' not in item:
                schema = BaseMeasureSchema()
            elif 'base_measures' in item:
                schema = DerivedMeasureSchema()
            else:
                raise ValidationError("Invalid measure type.")

            measure = schema.load(item)
            measures.append(measure)
        return measures


class MeasurableConceptSchema(Schema):
    class_name = fields.Str()
    name = fields.Str()
    value = fields.Float()
    impact = EnumField(Impact)
    entity = fields.Str()
    relevant_oss_aspect = EnumField(OSSAspect)
    information_need = fields.Str()
    quality_requirement = fields.Str()
    measures = MeasureField(many=True)

    @post_load
    def make_measurable_concept(self, data, **kwargs):
        return MeasurableConcept(**data)
