class MillError(Exception):
    """Base server error."""


class OauthError(MillError):
    """Error during oauth process."""


class InvalidStateError(OauthError):
    """Oauth state is invalid."""


class GetAccessTokenError(OauthError):
    """Error during getting access token."""


class ExternalAPIError(MillError):
    """Error with external API."""


class GitHubAPIError(ExternalAPIError):
    """GitHub API Error."""
