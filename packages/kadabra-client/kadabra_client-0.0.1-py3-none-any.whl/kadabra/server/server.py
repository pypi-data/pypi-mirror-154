from streamlit.server.server import Server as SLServer, State, SessionInfo
from streamlit.session_data import SessionData
from streamlit.watcher import LocalSourcesWatcher
from tornado.websocket import WebSocketHandler
from .app_session import AppSession
from logging import getLogger

logger = getLogger("kadabra.server.server")

# Code modified from Streamlit (Apache-2.0 license)
class Server(SLServer):
  def _create_app_session(self, ws: WebSocketHandler) -> AppSession:
    session_data = SessionData(self._main_script_path, self._command_line)
    local_sources_watcher = LocalSourcesWatcher(session_data)

    session = AppSession(
      ioloop=self._ioloop,
      session_data=session_data,
      uploaded_file_manager=self._uploaded_file_mgr,
      message_enqueued_callback=self._enqueued_some_message,
      local_sources_watcher=local_sources_watcher,
      user_info=dict()
    )

    logger.debug(
      "Created new session for ws %s. Session ID: %s", id(ws), session.id
    )

    assert (
      session.id not in self._session_info_by_id
    ), f"session.id '{session.id}' registered multiple times!"

    self._session_info_by_id[session.id] = SessionInfo(ws, session)
    self._set_state(State.ONE_OR_MORE_BROWSERS_CONNECTED)
    self._has_connection.notify_all()

    return session