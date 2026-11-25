from .db import conn

SORT_COLUMNS = {"title": "title", "due": "due", "owner": "owner", "id": "id"}


def list_tasks(project, sort="id", only_open=True):
    """Tasks of a project. `sort` comes from the query string."""
    column = SORT_COLUMNS.get(sort, "id")
    sql = f"SELECT * FROM tasks WHERE project = ? {'AND done = 0' if only_open else ''} ORDER BY {column}"
    return [dict(r) for r in conn().execute(sql, (project,))]


def tasks_for_owner(owner):
    return [dict(r) for r in conn().execute("SELECT * FROM tasks WHERE owner = ? ORDER BY due", (owner,))]
