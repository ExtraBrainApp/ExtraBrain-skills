# History, Settings, and App Controls

## History

Use `list_sessions`, `get_session`, and `search_sessions` for reads. `rename_session` is a narrow
metadata change. `delete_session` and `delete_session_insight` are destructive and require
explicit user intent. Delete sessions only one at a time: identify one exact session ID, call
`delete_session` once for that ID, and verify the remaining history before considering another
deletion. No bulk history-clear operation is supported. Summary and insight generation operate
on a known session ID; verify the resulting session resource.

## Non-secret settings

Read `extrabrain://settings`, then send a minimal `update_settings` patch with the current
settings revision. Preserve fields not named by the user. Credentials, provider URLs, licenses,
commerce, analytics identity, MCP security settings, profile arrays, internal updater state, and
local model paths are outside this tool.

Privacy preferences are writable but sensitive in effect. Change them only when the user
explicitly requests the particular behavior, then reread settings to verify it.

## App controls

Use the task-oriented capability listed by the live registry: `control_window`,
`set_remote_control`, `set_webcam_tracking`, `manage_permission`, `manage_local_model`,
`manage_update`, or `restart_app`. Never invent raw application actions.

Checking for or downloading an update can follow an explicit update request. Installing an
update and restarting ExtraBrain require that exact outcome to be explicit. Treat local-model
deletion and app restart as destructive even if a client annotation is less conservative.
