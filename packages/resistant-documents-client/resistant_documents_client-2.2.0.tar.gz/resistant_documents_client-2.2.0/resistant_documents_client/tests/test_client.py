import pytest
import requests_mock
from freezegun import freeze_time
from requests.exceptions import HTTPError

from resistant_documents_client.base import ResistantApiException
from resistant_documents_client.client import ResistantDocumentsClient
from resistant_documents_client.model import AnalysisFeedback

CLIENT_ID = "client1"
CLIENT_SECRET = "client_secret"
TOKEN_URL = "https://get.token.com/v1/token"
ACCESS_TOKEN = "abc"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

API_URL = "https://api.endpoint"
ENDPOINTS = ["fraud", "quality", "content", "decision"]


@pytest.fixture
def client_mock():
    with requests_mock.Mocker() as m:
        m.post(TOKEN_URL, json={"expires_in": 3600, "access_token": ACCESS_TOKEN})
        client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET, TOKEN_URL, API_URL)
        yield client, m


def test_token_refreshed_correctly():
    fraud_result = {"status_code": 200, "score": "HIGH_RISK"}
    with freeze_time() as frozen_datetime:
        with requests_mock.Mocker() as m:
            m.post(TOKEN_URL, json={"expires_in": 3600, "access_token": ACCESS_TOKEN})
            fraud_url = f'{API_URL}/v2/submission/id/fraud'
            m.get(fraud_url, request_headers=HEADERS, json=fraud_result)

            client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET, TOKEN_URL, API_URL)

            exp_url_history = [TOKEN_URL]
            for _ in range(3):
                assert fraud_result == client.fraud("id")
                exp_url_history.append(fraud_url)
            assert exp_url_history == [r.url for r in m.request_history]
            frozen_datetime.tick(3700)

            assert fraud_result == client.fraud("id")
            exp_url_history += [TOKEN_URL, fraud_url]
            assert exp_url_history == [r.url for r in m.request_history]


def test_submit(client_mock):
    client, m = client_mock
    desired_id = "id"
    m.post(f"{API_URL}/v2/submission", json={"upload_url": "https://test.upload/data", "submission_id": desired_id}, request_headers=HEADERS)
    m.put("https://test.upload/data", status_code=200)
    assert client.submit(b"abc", "query_1", "ONLY_QUALITY", enable_decision=True) == desired_id
    assert m.request_history[1].json() == {'pipeline_configuration': 'ONLY_QUALITY', 'query_id': 'query_1', 'enable_decision': True}


@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_endpoint_returns_data(client_mock, endpoint_name):
    client, m = client_mock
    result = {"message": "ok"}

    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', request_headers=HEADERS, json=result)
    assert result == getattr(client, endpoint_name)("id")


def test_submit_endpoint_retries(client_mock):
    client, m = client_mock
    responses = [{"status_code": 500}, {"status_code": 500}, {"json": {"upload_url": "https://test.upload/data", "submission_id": "id"}}]
    m.post(f"{API_URL}/v2/submission", response_list=responses, request_headers=HEADERS)
    m.put("https://test.upload/data", status_code=200)
    assert client.submit(b"abc", "query_1", "ONLY_QUALITY") == "id"


@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_poll_retries(client_mock, endpoint_name):
    client, m = client_mock
    result = {"message": "ok"}
    responses = [{"status_code": 404}, {"status_code": 404},
                 {"json": result, "status_code": 200}]

    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', responses)
    assert result == getattr(client, endpoint_name)("id")


@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_results_throws_exception_when_no_data_exists(client_mock, endpoint_name):
    client, m = client_mock
    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', status_code=404, request_headers=HEADERS)
    with pytest.raises(RuntimeError):
        getattr(client, endpoint_name)("id", max_num_retries=2)


def test_fraud_presign(client_mock):
    client, m = client_mock
    m.get(f'{API_URL}/v2/submission/id/fraud', status_code=400, request_headers=HEADERS)
    presign_s3_url = "https://s3.download.aws.com/some_object"
    m.get(f'{API_URL}/v2/submission/id/fraud?presign=true', status_code=200, json={"download_url": presign_s3_url}, request_headers=HEADERS)
    response = {"status": "SUCCESS"}
    m.get(presign_s3_url, json=response)

    act_response = client.fraud("id", 1)
    assert act_response == response


def test_client_proxy():
    no_proxy_client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET)
    assert no_proxy_client._api_session.proxies == {}
    assert no_proxy_client._s3_session.proxies == {}

    proxy_url = "proxy-url"
    proxy_client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET, proxy=proxy_url)
    assert proxy_client._api_session.proxies == {"https": proxy_url}
    assert proxy_client._s3_session.proxies == {"https": proxy_url}


@pytest.mark.parametrize("status, body, exception, message", [
    (200, {"analysis_feedback": "CORRECT", "comment": "comment", "updated": "2022-06-09T10:48:00Z"}, None, None),
    (404, None, None, None),
    (500, None, HTTPError, "500 Server Error"),
])
def test_feedback_get(client_mock, status, body, exception, message):
    client, m = client_mock
    m.get(f"{API_URL}/v2/submission/id/feedback", request_headers=HEADERS, status_code=status, json=body)

    if exception:
        with pytest.raises(exception, match=message):
            client.feedback("id")
    else:
        assert client.feedback("id") == body


@pytest.mark.parametrize("status, body, exception, message", [
    (200, {"analysis_feedback": "CORRECT", "comment": "comment", "updated": "2022-06-09T10:48:00Z"}, None, None),
    (404, None, ResistantApiException, "Add feedback failed, submission id not found"),
    (500, None, HTTPError, "500 Server Error"),
])
def test_feedback_put(client_mock, status, body, exception, message):
    client, m = client_mock
    m.put(f"{API_URL}/v2/submission/id/feedback", request_headers=HEADERS, status_code=status, json=body)

    if exception:
        with pytest.raises(exception, match=message):
            client.add_feedback("id", AnalysisFeedback.CORRECT, "comment")
    else:
        assert client.add_feedback("id", AnalysisFeedback.CORRECT, "comment") == body
    assert m.request_history[1].json() == {"analysis_feedback": "CORRECT", "comment": "comment"}


@pytest.mark.parametrize("status, exception, message", [
    (204, None, None),
    (404, ResistantApiException, "Delete submission failed, submission id not found"),
    (409, ResistantApiException, "Delete submission failed, submission id not ready"),
    (500, HTTPError, "500 Server Error"),
])
def test_delete(client_mock, status, exception, message):
    client, m = client_mock
    m.delete(f"{API_URL}/v2/submission/id", request_headers=HEADERS, status_code=status)

    if exception:
        with pytest.raises(exception, match=message):
            client.delete("id")
    else:
        assert client.delete("id") == None
