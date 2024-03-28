from typing import List

from ..base.logger import get_logger
from .html_view import HtmlView
from .md_view import MarkdownView

from ..database.db_schema import DbSchema


class ViewerRegistry:

    _viewers = {}

    @classmethod
    def register_viewer(cls, viewer):
        cls._viewers[viewer.format()] = viewer

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        return cls._viewers.keys()

    @classmethod
    def render(cls, db: DbSchema, format: str = "html"):
        viewer = cls._viewers.get(format)
        if not viewer:
            get_logger().error(f"No viewer found for format {format}")
            return
        return viewer.render(db)


ViewerRegistry.register_viewer(HtmlView)
ViewerRegistry.register_viewer(MarkdownView)
