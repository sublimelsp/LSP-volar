from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.protocol import TextDocumentSyncKindIncremental, TextDocumentSyncKindFull, TextDocumentSyncKindNone
from LSP.plugin.core.typing import List, Optional
from lsp_utils import NpmClientHandler
import os
import sublime
import subprocess


def plugin_loaded():
    LspVolarPlugin.setup()


def plugin_unloaded():
    LspVolarPlugin.cleanup()


class LspVolarPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'server'
    server_binary_path = os.path.join(server_directory, 'node_modules', '@volar', 'vue-language-server', 'bin', 'vue-language-server.js')

    @classmethod
    def is_allowed_to_start(
        cls,
        window: sublime.Window,
        initiating_view: Optional[sublime.View] = None,
        workspace_folders: Optional[List[WorkspaceFolder]] = None,
        configuration: Optional[ClientConfig] = None
    ):
        if not workspace_folders or not configuration:
            return
        configuration.init_options.set('textDocumentSync', get_text_document_sync(configuration))
        configuration.init_options.set('languageFeatures', get_language_features(configuration))
        configuration.init_options.set('documentFeatures', {
            "selectionRange": True,
            "foldingRange": True,
            "linkedEditingRange": False,
            "documentSymbol": True,
            "documentColor": True,
            "documentFormatting": {
                "defaultPrintWidth": 90
            }
        })
        if configuration.init_options.get('typescript.serverPath'):
            return  # don't find the `typescript.serverPath` if it was set explicitly in LSP-volar.sublime-settings
        typescript_path = cls.find_typescript_path(workspace_folders[0].path)
        configuration.init_options.set('typescript.serverPath', typescript_path)

    @classmethod
    def find_typescript_path(cls, current_folder: str) -> str:
        server_directory_path = cls._server_directory_path()
        resolve_module_script = os.path.join(server_directory_path, 'resolve_module.js')
        find_ts_server_command =  [cls._node_bin(), resolve_module_script, current_folder]
        startupinfo = None
        # Prevent cmd.exe popup on Windows.
        if sublime.platform() == "windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= (
                subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW
            )
        workspace_ts_path = subprocess.check_output(find_ts_server_command, universal_newlines=True, startupinfo=startupinfo)
        bundled_ts_path = os.path.join(server_directory_path, 'node_modules', 'typescript', 'lib', 'tsserverlibrary.js')
        return workspace_ts_path or bundled_ts_path


def get_default_tag_name_case(configuration: ClientConfig) -> str:
    preferred_tag_name_case = configuration.settings.get('volar.completion.preferredTagNameCase')
    if preferred_tag_name_case == 'kebab':
        return 'kebabCase'
    elif preferred_tag_name_case == 'pascal':
        return 'pascalCase'
    return 'both'


def get_default_attr_name_case(configuration: ClientConfig) -> str:
    preferred_attr_name_case = configuration.settings.get('volar.completion.preferredAttrNameCase')
    if preferred_attr_name_case == 'camel':
        return 'camelCase'
    return 'kebabCase'


def get_text_document_sync(configuration: ClientConfig) -> int:
    text_document_sync = configuration.settings.get('volar.vueserver.textDocumentSync')
    if text_document_sync == 'full':
        return TextDocumentSyncKindFull
    if text_document_sync == 'none':
        return TextDocumentSyncKindNone
    return TextDocumentSyncKindIncremental

def get_ignored_trigger_characters(configuration: ClientConfig) -> str:
    return configuration.settings.get('volar.completion.ignoreTriggerCharacters') or ""

def get_language_features(configuration: ClientConfig) -> dict:
    language_features = {
        "references": True,
        "implementation": True,
        "definition": True,
        "typeDefinition": True,
        "callHierarchy": False,
        "hover": True,
        "rename": True,
        "renameFileRefactoring": False,
        "signatureHelp": True,
        "codeAction": True,
        "workspaceSymbol": True,
        "completion": {
            "defaultTagNameCase": get_default_tag_name_case(configuration),
            "defaultAttrNameCase": get_default_attr_name_case(configuration),
            "getDocumentNameCasesRequest": False,
            "getDocumentSelectionRequest": False,
            "ignoreTriggerCharacters": get_ignored_trigger_characters(configuration)
        },
        "schemaRequestService": False,
        "documentHighlight": True,
        "documentLink": True,
        "codeLens": {"showReferencesNotification": True},
        "semanticTokens": True,
        "inlayHints": True,
        "diagnostics": True,
        "schemaRequestService": False
    }
    return language_features
