from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._metadata import SimpleObjectMetadata
    SimpleMetaType = SimpleObjectMetadata
else:
    SimpleMetaType = Any

