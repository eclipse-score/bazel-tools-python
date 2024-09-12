"""A collection of helper functions for the python aspect."""

_excluded_main_label_names = ["rules_python_entry_point_"]

_excluded_workspaces_roots = ["external/"]

def is_valid_label(label, excluded_labels = [], excluded_workspaces = []):
    """Check if a given label is valid.

    To validate a given label this functions checks its name and workspace.
    It already has a pre defined label and workspace exclusion list. It's,
     up to the user to provide additional exclusion lists or not.

    Args:
        label: label to be checked.
        excluded_labels: additional labels to exclude the given label from.
        excluded_workspaces: additional workspaces to exclude the given label from.
    Returns:
        True if the label is valid, and false otherwise.
    """

    for excluded_label in excluded_labels + _excluded_main_label_names:
        if excluded_label in label.name:
            return False
    for excluded_workspace_root in excluded_workspaces + _excluded_workspaces_roots:
        if excluded_workspace_root in label.workspace_root:
            return False
    return True
