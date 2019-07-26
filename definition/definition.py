class ValidationError(Exception):
    pass


class Definition(object):
    required_attributes = ['word', 'pronunciation', 'definition']
    remaining_attributes = ['source', 'example']

    def __init__(self, definition):
        for attr in (self.required_attributes + self.remaining_attributes):
            setattr(self, attr, definition.get(attr, '').strip())

        for attr in self.required_attributes:
            if getattr(self, attr) == '':
                raise ValidationError(f"Definition missing required field '{attr}'")

    def to_dict(self):
        return dict((key, value) for key, value in self.__dict__.items() if value != '')





