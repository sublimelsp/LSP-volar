from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import List, Optional, Union
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
    server_binary_path = os.path.join(server_directory, 'node_modules', '@volar', 'server', 'out', 'index.js')

    @classmethod
    def on_client_configuration_ready(cls, configuration: dict) -> None:
        is_lsp_typescript_enabled = sublime.load_settings("LSP-typescript.sublime-settings").get("enabled")
        take_over_mode = configuration.get("settings", {}).get("volar.takeOverMode.enabled", "auto") # type: Union[str, bool]

        def dont_start_in_ts_and_js_files():
            languages = configuration.get("languages", [])
            languages_without_typescript = list(filter(lambda langDict: langDict.get('languageId') not in ['typescript', "javascript"], languages))
            configuration['languages'] = languages_without_typescript

        if take_over_mode == "auto" and is_lsp_typescript_enabled:
            dont_start_in_ts_and_js_files()
        if take_over_mode == False:
            dont_start_in_ts_and_js_files()
        if take_over_mode == True and is_lsp_typescript_enabled:
            sublime.status_message('LSP-volar: \"volar.takeOverMode.enabled\" is enabled. Disable "LSP-typescript" or "LSP-volar" to avoid duplicate results.')

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
        if configuration.init_options.get('typescript.serverPath'):
            return # don't find the `typescript.serverPath` if it was set explicitly in LSP-volar.sublime-settings
        server_directory_path = cls._server_directory_path()
        resolve_module_script = os.path.join(server_directory_path, 'resolve_module.js')
        first_folder = workspace_folders[0].path
        command =  [cls._node_bin(), resolve_module_script, first_folder, 'typescript/lib/tsserverlibrary.js']
        workspace_ts_path = subprocess.check_output(command, universal_newlines=True)
        bundled_ts_path = os.path.join(server_directory_path, 'node_modules', 'typescript', 'lib', 'tsserverlibrary.js')
        configuration.init_options.set('typescript.serverPath', workspace_ts_path or bundled_ts_path)
