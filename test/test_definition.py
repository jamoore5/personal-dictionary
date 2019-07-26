from pytest import raises
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

    def test_word_required(self):
        definition = {'pronunciation': 'foo',
                      'definition': 'term used by programmers as a placeholder for a value that can change'}
        with raises(ValidationError) as error:
            Definition(definition)

        assert "Definition missing required field 'word'" in str(error)

    def test_pronunciation_required(self):
        definition = {'word': 'foo',
                      'definition': 'term used by programmers as a placeholder for a value that can change'}
        with raises(ValidationError) as error:
            Definition(definition)

        assert "Definition missing required field 'pronunciation'" in str(error)

    def test_definition_required(self):
        definition = {'word': 'foo', 'pronunciation': 'foo'}

        with raises(ValidationError) as error:
            Definition(definition)

        assert "Definition missing required field 'definition'" in str(error)


class TestToDict:
    def test_remove_empty_string_values(self):
        definition = Definition(
            {'word': 'foo', 'pronunciation': 'foo',
             'definition': 'term used by programmers as a placeholder for a value that can change',
             'source': '', 'example': ''}
        )

        dictionary = definition.to_dict()

        assert sorted(list(dictionary.keys())) == sorted(['word', 'pronunciation', 'definition'])
