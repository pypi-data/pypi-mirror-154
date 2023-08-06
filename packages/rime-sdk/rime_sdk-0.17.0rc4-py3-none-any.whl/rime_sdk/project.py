"""Library defining the interface to a project."""
from typing import NamedTuple

from rime_sdk.internal.backend import RIMEBackend
from rime_sdk.protos.project.project_pb2 import GetProjectRequest


class ProjectInfo(NamedTuple):
    """This object contains static information that describes a project."""

    project_id: str
    """How to refer to the project in the backend."""
    name: str
    """Name of the project."""
    description: str
    """Description of the project"""


class Project:
    """An interface to a RIME project.

    This object provides an interface for editing, updating, and deleting projects.

    Attributes:
        backend: RIMEBackend
            The RIME backend used to query about the status of the job.
        project_id: str
            The identifier for the RIME project that this object monitors.
    """

    def __init__(self, backend: RIMEBackend, project_id: str) -> None:
        """Contains information about a RIME Project.

        Args:
            backend: RIMEBackend
                The RIME backend used to query about the status of the job.
            project_id: str
                The identifier for the RIME project that this object monitors.
        """
        self._backend = backend
        self._project_id = project_id

    @property
    def project_id(self) -> str:
        """Return the id of this project."""
        return self._project_id

    @property
    def info(self) -> ProjectInfo:
        """Return information about this project."""
        project_req = GetProjectRequest(project_id=self._project_id)
        with self._backend.get_project_manager_stub() as project_manager:
            response = project_manager.GetProject(project_req)
        return ProjectInfo(
            self._project_id,
            response.project.project.name,
            response.project.project.description,
        )

    @property
    def name(self) -> str:
        """Return the name of this project."""
        return self.info.name

    @property
    def description(self) -> str:
        """Return the description of this project."""
        return self.info.description
