from LSP.plugin.core.typing import List, TypedDict
from LSP.plugin.core.protocol import Location, Position, TextDocumentIdentifier

VueFindReferencesParams = TypedDict('VueFindReferencesParams', {
    'position': Position,
    'references': List[Location],
    'textDocument': TextDocumentIdentifier,
})
