from __future__ import annotations
from collections.abc import Callable
from enum import IntEnum
from LSP.plugin import LspTextCommand
from LSP.plugin import LspWindowCommand
from LSP.plugin import Request
from LSP.plugin import Session
from LSP.plugin import uri_from_view
from LSP.plugin.core.promise import Promise
from LSP.plugin.core.tree_view import new_tree_view_sheet
from LSP.plugin.core.tree_view import TreeDataProvider
from LSP.plugin.core.tree_view import TreeItem
from LSP.plugin.core.views import text_document_identifier
from LSP.protocol import TextDocumentIdentifier
from LSP.protocol import URI
from os.path import basename
from typing import Any, NotRequired, Optional, TypedDict, Union
import sublime
import weakref


class FileKind(IntEnum):
    TextFile = 0
    TypeScriptHostFile = 1


class RenameDict(TypedDict):
    normalize: NotRequired[Callable[[str], str]]
    apply: NotRequired[Callable[[str], str]]

class CompletionDict(TypedDict):
    additional: NotRequired[bool]
    autoImportOnly: NotRequired[bool]

class FileCapabilities(TypedDict):
    diagnostic: NotRequired[bool]
    foldingRange: NotRequired[bool]
    documentFormatting: NotRequired[bool]
    documentSymbol: NotRequired[bool]
    codeAction: NotRequired[bool]
    inlayHint: NotRequired[bool]

class RenameCapabilities(TypedDict):
    normalize: Callable[[str], str]
    apply: NotRequired[Callable[[str], str]]

class CompletionCapabilities(TypedDict):
    additional: NotRequired[bool]
    autoImportOnly: NotRequired[bool]

class DiagnosticCapabilities(TypedDict):
    shouldReport: Callable[[], bool]

class FileRangeCapabilities(TypedDict):
    hover: NotRequired[bool]
    references: NotRequired[bool]
    definition: NotRequired[bool]
    rename: NotRequired[bool | RenameCapabilities]
    completion: NotRequired[bool | CompletionCapabilities]
    diagnostic: NotRequired[bool | DiagnosticCapabilities]
    semanticTokens: NotRequired[bool]
    referencesCodeLens: NotRequired[bool]
    displayWithLink: NotRequired[bool]

class Stack(TypedDict):
    source: str
    range: tuple[int, int]

class MirrorBehaviorCapabilities(TypedDict):
    references: NotRequired[bool]
    definition: NotRequired[bool]
    rename: NotRequired[bool]

class MappingFileRangeCapabilities(TypedDict):
    source: NotRequired[str]
    sourceRange: tuple[int, int]
    generatedRange: tuple[int, int]
    data: FileRangeCapabilities

class MappingMirrorBehaviorCapabilities(TypedDict):
    source: NotRequired[str]
    sourceRange: tuple[int, int]
    generatedRange: tuple[int, int]
    data: tuple[MirrorBehaviorCapabilities, MirrorBehaviorCapabilities]

class VirtualFile(TypedDict):
    fileName: str
    snapshot: Any
    kind: FileKind
    capabilities: FileCapabilities
    mappings: list[MappingFileRangeCapabilities]
    codegenStacks: list[Stack]
    mirrorBehaviorMappings: NotRequired[list[MappingMirrorBehaviorCapabilities]]
    embeddedFiles: list['VirtualFile']
    version: str


class GetVirtualFilesRequest:
    Type = 'volar/client/virtualFiles'
    ParamsType = TextDocumentIdentifier
    ResponseType = Optional[VirtualFile]

class GetVirtualFileRequestParamsType(TypedDict):
    sourceFileUri: str
    virtualFileName: str

class GetVirtualFileRequestResponseType(TypedDict):
    content: str
    mappings: dict[str, list[MappingFileRangeCapabilities]]
    codegenStacks: list[Stack]

class GetVirtualFileRequest:
    Type = 'volar/client/virtualFile'
    ParamsType = GetVirtualFileRequestParamsType
    ResponseType = GetVirtualFileRequestResponseType


class VirtualFilesDataProvider(TreeDataProvider):

    def __init__(
        self, weaksession: weakref.ref[Session], source_file_uri: str, root_elements: list[VirtualFile]
    ) -> None:
        self.weaksession = weaksession
        self.source_file_uri = source_file_uri
        self.root_elements = root_elements
        session = self.weaksession()
        self.session_name = session.config.name if session else None

    def get_children(self, element: VirtualFile | None) -> Promise[list[VirtualFile]]:
        if element is None:
            return Promise.resolve(self.root_elements)
        session = self.weaksession()
        if not session:
            return Promise.resolve([])
        return Promise.resolve(element['embeddedFiles'])

    def get_tree_item(self, element: VirtualFile) -> TreeItem:
        command_url = sublime.command_url('lsp_volar_open_virtual_file', {
            'uri': self.source_file_uri,
            'file_name': element['fileName'],
        })
        path = basename(element['fileName'])
        description = '(kind: {}, version: {})'.format(element['kind'], element['version'])
        return TreeItem(
            path,
            description=description,
            command_url=command_url
        )


class LspVolarShowVirtualFilesCommand(LspTextCommand):
    session_name = 'LSP-volar'

    def run(self, edit: sublime.Edit) -> None:
        sublime.set_timeout_async(self.run_async)

    def run_async(self) -> None:
        session = self.session_by_name()
        if not session:
            return
        request = Request(GetVirtualFilesRequest.Type, text_document_identifier(self.view), progress=True)
        session.send_request_task(request) \
            .then(lambda virtual_file: self._on_get_virtual_files_async(weakref.ref(session), virtual_file))

    def _on_get_virtual_files_async(
        self, weaksession: weakref.ref[Session], virtual_file: GetVirtualFilesRequest.ResponseType
    ) -> None:
        if not virtual_file:
            sublime.status_message('No virtual file found')
            return
        window = self.view.window()
        if not window:
            return
        session = weaksession()
        if not session:
            return
        sheet_name = 'Virtual Files (LSP-volar)'
        source_file_uri = uri_from_view(self.view)
        elements = [virtual_file]
        data_provider = VirtualFilesDataProvider(weaksession, source_file_uri, elements)
        new_tree_view_sheet(window, sheet_name, data_provider, sheet_name)
        window.run_command('lsp_volar_open_virtual_file', {
            'uri': source_file_uri,
            'file_name': virtual_file['fileName'],
        })


class LspVolarOpenVirtualFileCommand(LspWindowCommand):
    session_name = 'LSP-volar'

    def run(self, uri: str, file_name: str, event: dict | None = None) -> None:
        sublime.set_timeout_async(lambda: self.run_async(uri, file_name))

    def run_async(self, uri: str, file_name: str) -> None:
        session = self.session()
        if not session:
            return
        request = Request(GetVirtualFileRequest.Type, {
            'sourceFileUri': uri,
            'virtualFileName': file_name,
        })
        session.send_request_task(request).then(lambda result: self._on_files_contents_async(uri, file_name, result))

    def _on_files_contents_async(self, uri: URI, file_name: str, result: GetVirtualFileRequest.ResponseType) -> None:
        flags = sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT | sublime.CLEAR_TO_RIGHT
        # Force TS syntax for virtual .js files.
        # Those are actually TS files and using .js extension triggers errors from LSP.
        if file_name.endswith('.js'):
            file_name += '.ts'
        syntax = sublime.find_syntax_for_file(file_name)
        syntax_path = syntax.path if syntax else 'scope:source.ts'
        new_view = self.window.new_file(flags=flags, syntax=syntax_path)
        if new_view:
            new_view.set_scratch(True)
            new_view.set_name(f'(virtual) {uri}')
            new_view.run_command('append', {'characters': result['content']})
