from __future__ import annotations

from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import PluginStartError
from lsp_utils import NodeManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing_extensions import override


def plugin_loaded():
    LspVolarPlugin.register()


def plugin_unloaded():
    LspVolarPlugin.unregister()


class LspVolarPlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        if not context.workspace_folders:
            raise PluginStartError('Can not run without a workspace folder')
        package_name = cls.plugin_storage_path.name
        server_directory_path = NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath('Packages', package_name, 'language-server'),
            Path('node_modules', '@vue', 'language-server', 'bin', 'vue-language-server.js'),
            '>=16',
        )
        if not context.configuration.initialization_options.get('typescript.tsdk'):
            if not server_directory_path:
                raise PluginStartError('Could not start server without "typescript.sdk" being set.')
            typescript_lib_path = cls.find_typescript_lib_path(
                context.workspace_folders[0].path, server_directory_path)
            if not typescript_lib_path:
                raise PluginStartError('Could not resolve location of TypeScript package')
            context.configuration.initialization_options.set('typescript.tsdk', typescript_lib_path)

    @classmethod
    def find_typescript_lib_path(cls, workspace_folder: str, server_directory_path: Path) -> Path | None:
        module_paths = [
            'node_modules/typescript/lib/tsserverlibrary.js',
            '.vscode/pnpify/typescript/lib/tsserverlibrary.js',
            '.yarn/sdks/typescript/lib/tsserverlibrary.js'
        ]
        for module_path in module_paths:
            candidate = Path(workspace_folder, module_path)
            if candidate.is_file():
                return candidate.parent
        return server_directory_path / 'node_modules' / 'typescript' / 'lib'
