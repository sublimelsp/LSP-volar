from .plugin_types import VueFindReferencesParams
from LSP.plugin import ClientConfig
from LSP.plugin import WorkspaceFolder
from LSP.plugin.core.typing import List, Optional
from LSP.plugin.locationpicker import LocationPicker
from lsp_utils import NpmClientHandler, notification_handler
import os
import sublime


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
    ) -> Optional[str]:
        if not workspace_folders or not configuration:
            return 'Can not run without a workspace folder'
        if configuration.init_options.get('typescript.tsdk'):
            return  # don't find the `typescript.tsdk` if it was set explicitly in LSP-volar.sublime-settings
        typescript_lib_path = cls.find_typescript_lib_path(workspace_folders[0].path)
        if not typescript_lib_path:
            return 'Could not resolve location of TypeScript package'
        configuration.init_options.set('typescript.tsdk', typescript_lib_path)

    @classmethod
    def find_typescript_lib_path(cls, workspace_folder: str) -> Optional[str]:
        module_paths = [
            'node_modules/typescript/lib/tsserverlibrary.js',
            '.vscode/pnpify/typescript/lib/tsserverlibrary.js',
            '.yarn/sdks/typescript/lib/tsserverlibrary.js'
        ]
        for module_path in module_paths:
            candidate = os.path.join(workspace_folder, module_path)
            if os.path.isfile(candidate):
                return os.path.dirname(candidate)
        server_directory_path = cls._server_directory_path()
        return os.path.join(server_directory_path, 'node_modules', 'typescript', 'lib')

    @notification_handler('vue.findReferences')
    def onVueFindReferences(self, params: VueFindReferencesParams) -> None:
        session = self.weaksession()
        if not session:
            return
        view = sublime.active_window().active_view()
        if not view:
            return
        references = params['references']
        if len(references) == 1:
            args = {
                'location': references[0],
                'session_name': session.config.name,
            }
            view.run_command('lsp_open_location', args)
        elif references:
            LocationPicker(view, session, params['references'], side_by_side=False)
        else:
            sublime.status_message('No references found')
