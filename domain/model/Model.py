from marshmallow import fields, ValidationError, post_load, Schema, INCLUDE

from domain.model.Characteristic import Characteristic
from domain.model.Measure import BaseMeasure, DerivedMeasure, MeasurementMethod
from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact
from domain.model.QualityModel import QualityModel
from domain.model.SubCharacteristic import SubCharacteristic
from domain.model.Viewpoint import Viewpoint
from util.Util import load_class_from_file_path


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
            raise ValidationError(f"Invalid value '{value}' for field '{attr}'")


class MeasureSchema(Schema):
    name = fields.Str(required=True)
    value = fields.Raw(allow_none=True)
    unit = fields.Str()
    scale = fields.Float()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_measure(self, data, **kwargs):
        if isinstance(data, BaseMeasure) or isinstance(data, DerivedMeasure):
            return data
        if 'base_measures' in data:
            schema = DerivedMeasureSchema()
        else:
            schema = BaseMeasureSchema()
        return schema.load(data)


class BaseMeasureSchema(MeasureSchema):
    visitor = fields.Str(required=True)
    measurement_method = EnumField(MeasurementMethod)

    @post_load
    def make_base_measure(self, data, **kwargs):
        visitor_path = data.pop('visitor')
        visitor = load_class_from_file_path(visitor_path)
        data['visitor'] = visitor
        return BaseMeasure(**data)


class DerivedMeasureSchema(MeasureSchema):
    base_measures = fields.List(fields.Nested(lambda: 'MeasureSchema'), default=[])
    normalize_visitor = fields.Str(required=True)
    aggregate_visitor = fields.Str(required=True)
    measurement_method = EnumField(MeasurementMethod)

    @post_load
    def make_derived_measure(self, data, **kwargs):
        children = {child.name: child for child in data.pop('base_measures')}
        data['children'] = children

        normalize_visitor_path = data.pop('normalize_visitor')
        normalize_visitor = load_class_from_file_path(normalize_visitor_path)
        data['normalize_visitor'] = normalize_visitor

        aggregate_visitor_path = data.pop('aggregate_visitor')
        aggregate_visitor = load_class_from_file_path(aggregate_visitor_path)
        data['aggregate_visitor'] = aggregate_visitor

        return DerivedMeasure(**data)


class MeasurableConceptSchema(Schema):
    name = fields.Str()
    value = fields.Float()
    impact = EnumField(Impact)
    entity = fields.Str()
    relevant_oss_aspect = EnumField(OSSAspect)
    information_need = fields.Str()
    quality_requirement = fields.Str()
    normalize_visitor = fields.Str(required=True)
    aggregate_visitor = fields.Str(required=True)
    measures = fields.List(fields.Nested(lambda: MeasureSchema()), default=[])

    @post_load
    def make_measurable_concept(self, data, **kwargs):
        children = {child.name: child for child in data.pop('measures')}
        data['children'] = children

        normalize_visitor_path = data.pop('normalize_visitor')
        normalize_visitor = load_class_from_file_path(normalize_visitor_path)
        data['normalize_visitor'] = normalize_visitor

        aggregate_visitor_path = data.pop('aggregate_visitor')
        aggregate_visitor = load_class_from_file_path(aggregate_visitor_path)
        data['aggregate_visitor'] = aggregate_visitor

        return MeasurableConcept(**data)


class SubCharacteristicSchema(Schema):
    name = fields.Str()
    measurable_concepts = fields.List(fields.Nested(lambda: MeasurableConceptSchema()), default=[])

    @post_load
    def make_sub_characteristic(self, data, **kwargs):
        children = {child.name: child for child in data.pop('measurable_concepts')}
        data['children'] = children
        return SubCharacteristic(**data)


class CharacteristicSchema(Schema):
    name = fields.Str()
    sub_characteristics = fields.List(fields.Nested(lambda: SubCharacteristicSchema()), default=[])

    @post_load
    def make_characteristic(self, data, **kwargs):
        children = {child.name: child for child in data.pop('sub_characteristics')}
        data['children'] = children
        return Characteristic(**data)


class ViewpointSchema(Schema):
    name = fields.Str()
    characteristics = fields.List(fields.Nested(lambda: CharacteristicSchema()), default=[])

    @post_load
    def make_viewpoint(self, data, **kwargs):
        children = {child.name: child for child in data.pop('characteristics')}
        data['children'] = children
        return Viewpoint(**data)


class QualityModelSchema(Schema):
    name = fields.Str()
    viewpoints = fields.List(fields.Nested(lambda: ViewpointSchema()), default=[])

    @post_load
    def make_quality_model(self, data, **kwargs):
        children = {child.name: child for child in data.pop('viewpoints')}
        data['children'] = children
        return QualityModel(**data)
