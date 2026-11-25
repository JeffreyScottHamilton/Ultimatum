import os
import subprocess


def export_project(project: str, attachments_dir: str, out_dir: str) -> str:
    """Zip the attachments of `project`; `project` is the project name typed by the user."""
    archive = os.path.join(out_dir, f"{project}.zip")
    subprocess.run(f"zip -rq {archive} {attachments_dir}", shell=True, check=True)
    return archive
