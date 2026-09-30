# Live Session Operations

Read `extrabrain://state` and `extrabrain://current-session` before live operations.

- `start_session` starts at most one session and consumes preparation only after successful
  startup. Pass the revision just verified from `extrabrain://preparation/next` as
  `expectedPreparationRevision`. The revision can be nonzero when `preparation` is null because
  successful consumption advances it. Call it only on an explicit start or record request.
- `stop_session` stops the active recording. Call it only on an explicit stop request.
- `reset_current_session_view` clears the inactive current view; it does not delete history.
- `start_analysis` may include a focused directive or follow-up. Use `cancel_analysis` only for a
  known in-progress analysis ID.
- `submit_session_chat` asks against the active session context. Cancel only the identified turn.
- `capture_screen`, `capture_region`, `delete_screenshot`, and `set_mute_state` act on live capture
  state. Confirm the session is active where the capability contract requires it.

After a state-changing call, reread current state. Do not repeatedly retry a still-running
operation with new IDs; first determine whether it is already in progress or completed.
