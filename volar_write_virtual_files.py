from LSP.plugin import LspTextCommand
from LSP.plugin import Notification
from LSP.plugin.core.protocol import TextDocumentIdentifier
from LSP.plugin.core.views import uri_from_view
import sublime


class WriteVirtualFilesNotification:
    Type = 'volar/client/writeVirtualFiles'
    ParamsType = TextDocumentIdentifier


class LspVolarWriteVirtualFilesCommand(LspTextCommand):
    session_name = 'LSP-volar'

    def run(self, edit: sublime.Edit) -> None:
        sublime.set_timeout_async(self.run_async)

    def run_async(self) -> None:
        session = self.session_by_name()
        if not session:
            return
        session.send_notification(Notification(WriteVirtualFilesNotification.Type, {'uri': uri_from_view(self.view)}))
