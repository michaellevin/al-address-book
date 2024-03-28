import unittest
from unittest.mock import patch
from pathlib import Path
from address_app.serialize import (
    SerializeStrategyRegistry,
    get_supported_formats,
)
from address_app.base.consts import DEFAULT_ROOT_PATH, RELATIVE_STORAGE_PATH
from address_app.database.db_schema import DbSchema


class TestSerialize(unittest.TestCase):

    def test_serialize(self):
        db_schema = DbSchema()
        db_schema.books = {"TestBook": [3914141904]}
        db_schema.contacts = {
            3914141904: {
                "name": "John Doe",
                "address": "123 Main St",
                "phone_no": "555-1234",
            }
        }

        self.json_strategy = SerializeStrategyRegistry.get_strategy_for_extension(
            "json"
        )
        json_res = self.json_strategy.serialize(db_schema)
        self.assertEqual(
            json_res,
            '{"contacts": {"3914141904": {"name": "John Doe", "address": "123 Main St", "phone_no": "555-1234"}}, "books": {"TestBook": [3914141904]}}',
            "Should serialize to json",
        )

        self.yaml_strategy = SerializeStrategyRegistry.get_strategy_for_extension(
            "yaml"
        )
        yaml_res = self.yaml_strategy.serialize(db_schema)
        # print(yaml_res)

        self.assertEqual(
            len(get_supported_formats()), 3, "Should have 3 supported formats"
        )

        res_db_schema = self.json_strategy.deserialize(json_res)
        self.assertEqual(
            db_schema, res_db_schema, "Should deserialize to original schema"
        )

    def tearDown(self) -> None:
        # self.file_storage.delete()
        pass


if __name__ == "__main__":
    unittest.main()
