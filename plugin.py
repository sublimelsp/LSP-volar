from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import List, Optional
from lsp_utils import NpmClientHandler
import os
import sublime
import subprocess


def plugin_loaded():
    LspVolarPlugin.setup()
    LspVolarSecondServer.setup()


def plugin_unloaded():
    LspVolarPlugin.cleanup()
    LspVolarSecondServer.cleanup()


document_features = {
    "selectionRange": True,
    "foldingRange": True,
    "linkedEditingRange": False,
    "documentSymbol": True,
    "documentColor": True,
    "documentFormatting": {
        "defaultPrintWidth": 90
    }
}


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
        configuration.init_options.set('languageFeatures', get_language_features(configuration, is_main_server=True))
        configuration.init_options.set('documentFeatures', document_features)
        if configuration.init_options.get('typescript.serverPath'):
            return  # don't find the `typescript.serverPath` if it was set explicitly in LSP-volar.sublime-settings
        typescript_path = find_typescript_path(LspVolarPlugin, workspace_folders[0].path)
        configuration.init_options.set('typescript.serverPath', typescript_path)


class LspVolarSecondServer(LspVolarPlugin):
    @classmethod
    def get_displayed_name(cls) -> str:
        return 'LSP-volar(second server)'

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
        use_second_server = configuration.settings.get('volar.vueserver.useSecondServer')
        if not use_second_server:
            return "Not enabled"
        configuration.init_options.set('languageFeatures', get_language_features(configuration, is_main_server=False))
        configuration.init_options.set('documentFeatures', document_features)
        if configuration.init_options.get('typescript.serverPath'):
            return  # don't find the `typescript.serverPath` if it was set explicitly in LSP-volar.sublime-settings
        typescript_path = find_typescript_path(LspVolarSecondServer, workspace_folders[0].path)
        configuration.init_options.set('typescript.serverPath', typescript_path)


def find_typescript_path(plugin, current_folder: str) -> str:
    server_directory_path = plugin._server_directory_path()
    resolve_module_script = os.path.join(server_directory_path, 'resolve_module.js')
    find_ts_server_command =  [plugin._node_bin(), resolve_module_script, current_folder]
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


def get_language_features(configuration: ClientConfig, is_main_server: bool) -> dict:
    use_second_server = configuration.settings.get('volar.vueserver.useSecondServer')
    main_language_features = {
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
        },
        "schemaRequestService": False
    }
    second_language_features = {
        "documentHighlight": True,
        "documentLink": True,
        "codeLens": {"showReferencesNotification": True},
        "semanticTokens": True,
        "inlayHints": False,
        "diagnostics": True,
        "schemaRequestService": False
    }
    if is_main_server:
        all_language_features = {}
        all_language_features.update(main_language_features)
        all_language_features.update(second_language_features)
        return main_language_features if use_second_server else all_language_features
    return second_language_features
