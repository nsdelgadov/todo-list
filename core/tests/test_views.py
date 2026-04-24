from django.urls import reverse


def test_index_returns_200_with_ok_body(client):
    response = client.get(reverse("core:index"))

    assert response.status_code == 200
    assert response.content == b"Django OK"
