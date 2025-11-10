from src.utils.logging_utils import log_error
def read_sql_helper(path: str) -> str | None:
    """Read a SQL script from a file and return its content as a string.

    Args:
        path: Path to the SQL file.

    Returns:
        The SQL script as a string, or None if an error occurs.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        log_error(f"Error reading SQL script {str}: {e}")
        return None
