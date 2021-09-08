from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
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
    server_binary_path = os.path.join(server_directory, 'node_modules', '@volar', 'server', 'out', 'index.js')

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
        resolve_module_script = os.path.join(cls._server_directory_path(), 'resolve_module.js')
        first_folder = workspace_folders[0].path
        workspace_ts_path = subprocess.check_output([cls._node_bin(), resolve_module_script, first_folder, 'typescript/lib/tsserverlibrary.js']).decode('utf-8', 'ignore')
        bundled_ts_path = os.path.join(cls._server_directory_path(), 'node_modules', 'typescript', 'lib', 'tsserverlibrary.js')
        configuration.init_options.set('typescript.serverPath', workspace_ts_path or bundled_ts_path)