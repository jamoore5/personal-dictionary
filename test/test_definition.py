import pytest
from definition.definition import Definition, ValidationError


class TestInitialize:
    def test_strips_whitespace(self):
        definition = Definition(
            {'word': '  foo  ', 'pronunciation': '  foo  ',
             'definition': '  term used by programmers as a placeholder for a value that can change  '}
        )

        assert definition.word == 'foo'
        assert definition.pronunciation == 'foo'
        assert definition.definition == 'term used by programmers as a placeholder for a value that can change'

    @pytest.mark.parametrize("definition,missing_field", [
        ({'pronunciation': 'p', 'definition': 'd'}, 'word'),
        ({'word': 'w', 'definition': 'd'}, 'pronunciation'),
        ({'word': 'w', 'pronunciation': 'p'}, 'definition'),
        ({'word': '', 'pronunciation': 'p', 'definition': 'd'}, 'word'),
        ({'word': 'w', 'pronunciation': '', 'definition': 'd'}, 'pronunciation'),
        ({'word': 'w', 'pronunciation': 'p', 'definition': ''}, 'definition')
    ])
    def test_missing_required_field(self, definition, missing_field):
        with pytest.raises(ValidationError) as error:
            Definition(definition)

        assert f"Definition missing required field '{missing_field}'" in str(error)


class TestToDict:
    def test_remove_empty_string_values(self):
        definition = Definition(
            {'word': 'foo', 'pronunciation': 'foo',
             'definition': 'term used by programmers as a placeholder for a value that can change',
             'source': '', 'example': ''}
        )

        dictionary = definition.to_dict()

        assert sorted(list(dictionary.keys())) == sorted(['word', 'pronunciation', 'definition'])
