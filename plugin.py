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
        ts_path = ''
        resolve_module_script = os.path.join(cls._server_directory_path(), 'resolve_module.js')
        first_folder = workspace_folders[0].path
        proc = subprocess.Popen(['node', resolve_module_script, first_folder, 'typescript/lib/tsserverlibrary.js'], stdout=subprocess.PIPE)
        if proc.stdout:
            ts_path = proc.stdout.read().decode('utf-8', 'ignore') # workspace ts path
        if not ts_path:
            ts_path = os.path.join(cls._server_directory_path(), 'node_modules', 'typescript', 'lib', 'tsserverlibrary.js') # bundled ts path
        configuration.init_options.set('typescript.serverPath', ts_path)