from voda_sdk.http.sdk import HttpSDK


def create_session(server_url: str, api_key: str) -> HttpSDK:
    """
    Create http client session for VODA SDK

    :param server_url: Server url for VODA Core
    :param api_key: Api Key for VODA Core SDK
    :return:
    """
    return HttpSDK(server_url, api_key)
