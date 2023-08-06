from enum import auto
from enum import IntEnum

from furl import Path as UrlPath
from furl.furl import furl as Url
from requests.models import Response
from testlodge.api.base import BaseAPI
from testlodge.typing.plan_content import PlanContentJSON
from testlodge.typing.plan_content import PlantContentListJSON


class PlanContentAPI(BaseAPI):
    """API for test plan content.

    Endpoints
    ---------
    * List
    * Show
    * Create
    * Update
    * Delete
    """

    name: str = 'plan_content'

    def _list(
        self,
        *,
        project_id: int,
        plan_id: int,
        page: int = 1,
    ) -> PlantContentListJSON:
        """Paginated list of all plan content in a plan.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        plan_id: int
            The ID of the plan.
        page: int, default=1
            Default: 1
            The number of the page to return.
        """

        method = 'GET'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}/plans/{plan_id}/plan_contents.json'
        )
        params: dict = {}
        if page != 1:
            params['page'] = page

        response: Response = self.client._request(
            method=method, url=url, params=params
        )
        plan_content_list: PlantContentListJSON = response.json()

        return plan_content_list

    def _show(
        self,
        *,
        project_id: int,
        plan_id: int,
        plan_content_id: int,
    ) -> PlanContentJSON:
        """Get the details for a plan content item.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        plan_id: int
            The ID of the plan content.
        plan_content_id: int
            The ID of the plan content.
        """

        method = 'GET'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}/plans/{plan_id}/plan_contents/{plan_content_id}.json'
        )

        response: Response = self.client._request(
            method=method,
            url=url,
        )
        plan_content_json: PlanContentJSON = response.json()

        return plan_content_json

    def _create(
        self,
        *,
        project_id: int,
        plan_id: int,
        plan_content: PlanContentJSON,
    ) -> PlanContentJSON:
        """Create a new test plan content.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        plan_id: int
            The ID of the plan content.
        plan_content: PlanContentJSON

            title: str
                The test plan content title / heading (Required)
            content: str
                The body text of content
            custom_fields:
                ...
        """

        method = 'POST'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}/plans/{plan_id}/plan_contents.json'
        )

        data = dict(plan_content=plan_content)

        response: Response = self.client._request(
            method=method, url=url, json=data
        )
        plan_content_json: PlanContentJSON = response.json()

        return plan_content_json

    def _update(
        self,
        *,
        project_id: int,
        plan_id: int,
        plan_content_id: int,
        plan_content: PlanContentJSON,
    ) -> PlanContentJSON:
        """Update a plan content item.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        plan_id: int
            The ID of the plan.
        plan_content_id: int
            The ID of the plan content.
        plan_content: PlanContentJSON

            title: str
                The test plan content title / heading (Required)
            content: str
                The body text of content
            custom_fields:
                ...
        """

        method = 'PATCH'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}/plans/{plan_id}/plan_contents/{plan_content_id}.json'
        )

        data = dict(plan_content=plan_content)

        response: Response = self.client._request(
            method=method,
            url=url,
            json=data,
        )
        plan_content_json: PlanContentJSON = response.json()

        return plan_content_json

    def _delete(
        self, *, project_id: int, plan_id: int, plan_content_id: int
    ) -> None:
        """Delete a plan content item.

        Parameters
        ----------
        project_id: int
            The ID of the project.
        plan_id: int
            The ID of the plan.
        plan_content_id: int
            The ID of the plan content.
        """

        method = 'DELETE'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}/plans/{plan_id}/plan_contents/{plan_content_id}.json'
        )

        response: Response = self.client._request(method=method, url=url)

        status_code: int = response.status_code
        if status_code != 204:
            print(f'Unexpected response code: {status_code}')

        return None
