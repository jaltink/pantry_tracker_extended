# pantry_tracker/webapp/schemas.py - UITGEBREIDE VERSIE
from marshmallow import Schema, fields, validate, validates, ValidationError

class CategorySchema(Schema):
    """Schema for creating a new category."""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class UpdateCategorySchema(Schema):
    """Schema for updating an existing category's name."""
    new_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    
    @validates('new_name')
    def validate_new_name(self, value):
        if not value.strip():
            raise ValidationError("New category name cannot be empty or whitespace.")

class LocationSchema(Schema):
    """Schema for creating/updating locations - NIEUW"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=200))

class ProductSchema(Schema):
    """Schema for creating a new product - UITGEBREID"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    url = fields.Url(required=True, validate=validate.Length(max=200))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    barcode = fields.Str(required=False, allow_none=True, validate=validate.Length(min=8, max=13))
    image_front_small_url = fields.Str(required=False, allow_none=True, validate=validate.URL())
    
    # NIEUWE VELDEN
    min_stock = fields.Int(required=False, load_default=5, validate=validate.Range(min=0, max=1000))
    location = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1, max=50))
    expiry_date = fields.Date(required=False, allow_none=True)
    notes = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    
    @validates('barcode')
    def validate_barcode(self, value):
        if value and not value.isdigit():
            raise ValidationError("Barcode must be numeric.")
        if value and not (8 <= len(value) <= 13):
            raise ValidationError("Barcode must be between 8 to 13 digits.")

class UpdateProductSchema(Schema):
    """Schema for updating an existing product - UITGEBREID"""
    new_name = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    url = fields.Url(required=False, validate=validate.Length(max=200))
    barcode = fields.Str(required=False, allow_none=True, validate=validate.Length(min=8, max=13))
    image_front_small_url = fields.Str(required=False, allow_none=True, validate=validate.URL())
    
    # NIEUWE VELDEN
    min_stock = fields.Int(required=False, validate=validate.Range(min=0, max=1000))
    location = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1, max=50))
    expiry_date = fields.Date(required=False, allow_none=True)
    notes = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    
    @validates('barcode')
    def validate_barcode(self, value):
        if value is not None:
            if value and not value.isdigit():
                raise ValidationError("Barcode must be numeric.")
            if value and not (8 <= len(value) <= 13):
                raise ValidationError("Barcode must be between 8 to 13 digits.")
