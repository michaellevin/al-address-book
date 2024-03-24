from .base_serialization import SerializeStrategy


class XMLStrategy(SerializeStrategy):
    @classmethod
    def get_supported_extensions(cls) -> str:
        return ("xml",)

    @classmethod
    def serialize(cls, data: dict, url: str):
        import xml.etree.ElementTree as ET
        import os

        os.makedirs(os.path.dirname(url), exist_ok=True)

        def _dict_to_xml(data: dict, parent: ET.Element):
            for key, value in data.items():
                if isinstance(value, dict):
                    sub_element = ET.SubElement(parent, key)
                    _dict_to_xml(value, sub_element)
                elif isinstance(value, list):
                    for item in value:
                        item_element = ET.SubElement(parent, key)
                        if isinstance(item, dict):
                            _dict_to_xml(item, item_element)
                        else:
                            item_element.text = str(item)
                else:
                    child = ET.SubElement(parent, key)
                    child.text = str(value)

        root = ET.Element("root")
        _dict_to_xml(data, root)
        tree = ET.ElementTree(root)

        with open(url, "w", encoding="UTF-8") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(file, encoding="unicode")
