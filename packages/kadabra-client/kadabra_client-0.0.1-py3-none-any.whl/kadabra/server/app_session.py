from streamlit.app_session import AppSession as SLAppSession
from streamlit.scriptrunner import RerunData
from .script_runner import ScriptRunner

# Code modified from Streamlit (Apache-2.0 license)
class AppSession(SLAppSession):
  def _create_scriptrunner(self, initial_rerun_data: RerunData) -> None:
    self._scriptrunner = ScriptRunner(
      session_id=self.id,
      session_data=self._session_data,
      client_state=self._client_state,
      session_state=self._session_state,
      uploaded_file_mgr=self._uploaded_file_mgr,
      initial_rerun_data=initial_rerun_data,
      user_info=self._user_info,
    )
    self._scriptrunner.on_event.connect(self._on_scriptrunner_event)
    self._scriptrunner.start()
