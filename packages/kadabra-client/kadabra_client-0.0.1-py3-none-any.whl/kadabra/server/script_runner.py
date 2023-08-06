from streamlit.scriptrunner import ScriptRunner as SLScriptRunner, ScriptRunnerEvent
from streamlit.session_data import SessionData
from streamlit.error_util import handle_uncaught_app_exception
from streamlit.state import SessionState, SCRIPT_RUN_WITHOUT_ERRORS_KEY
from streamlit import source_util
from streamlit.in_memory_file_manager import in_memory_file_manager
from streamlit.scriptrunner.script_requests import RerunData
from logging import getLogger
from ..kernel.shell import Shell

logger = getLogger("kadabra.server.script_runner")

# Code modified from Streamlit (Apache-2.0 license)
class ScriptRunner(SLScriptRunner):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.shell = Shell.instance()

  def _run_script(self, rerun_data: RerunData) -> None:
    assert self._is_in_script_thread()
    logger.debug("Running script %s", rerun_data)
    in_memory_file_manager.clear_session_files()
    main_script_path = self._session_data.main_script_path
    pages = source_util.get_pages(main_script_path)
    current_page_info = list(pages.values())[0]
    page_script_hash = current_page_info["page_script_hash"]
    ctx = self._get_script_run_ctx()
    ctx.reset(
      query_string=rerun_data.query_string,
      page_script_hash=page_script_hash,
    )
    self.on_event.send(
      self,
      event=ScriptRunnerEvent.SCRIPT_STARTED,
      page_script_hash=page_script_hash,
    )

    script_path = current_page_info['script_path']
    with source_util.open_python_file(script_path) as f:
      filebody = f.read()
    
    ctx.on_script_start()

    res = self.shell.run_cell(filebody)
    if res.error_before_exec is not None:
      logger.debug("Fatal script error: %s", res.error_before_exec)
      self._session_state[SCRIPT_RUN_WITHOUT_ERRORS_KEY] = False
      self.on_event.send(
          self,
          event=ScriptRunnerEvent.SCRIPT_STOPPED_WITH_COMPILE_ERROR,
          exception=res.error_before_exec,
      )
      return
    elif res.error_in_exec is not None:
      self._session_state[SCRIPT_RUN_WITHOUT_ERRORS_KEY] = False
      handle_uncaught_app_exception(res.error_in_exec)
    else:
      self._session_state[SCRIPT_RUN_WITHOUT_ERRORS_KEY] = False

    self._on_script_finished(ctx)
