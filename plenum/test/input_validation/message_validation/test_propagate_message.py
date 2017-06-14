import pytest
from plenum.common.types import Propagate, ClientMessageValidator
from collections import OrderedDict
from plenum.common.messages.fields import NonNegativeNumberField, \
    LedgerIdField, MerkleRootField, IterableField, NonEmptyStringField, \
    TimestampField, HexField

EXPECTED_ORDERED_FIELDS = OrderedDict([
    ("request", ClientMessageValidator),
    ("senderClient", NonEmptyStringField),
])


def test_hash_expected_type():
    assert Propagate.typename == "PROPAGATE"


def test_has_expected_fields():
    actual_field_names = OrderedDict(Propagate.schema).keys()
    assert actual_field_names == EXPECTED_ORDERED_FIELDS.keys()


def test_has_expected_validators():
    schema = dict(Propagate.schema)
    for field, validator in EXPECTED_ORDERED_FIELDS.items():
        assert isinstance(schema[field], validator)