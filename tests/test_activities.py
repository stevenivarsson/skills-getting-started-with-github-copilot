import urllib.parse


def _quote(name: str) -> str:
    return urllib.parse.quote(name, safe="")


def test_get_activities_returns_all(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_new_student(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    path = f"/activities/{_quote(activity)}/signup"
    r = client.post(path, params={"email": email})
    assert r.status_code == 200
    assert email in r.json()["message"]
    # verify participants updated
    r2 = client.get("/activities")
    assert email in r2.json()[activity]["participants"]


def test_signup_existing_student_returns_400(client):
    activity = "Chess Club"
    existing = "michael@mergington.edu"
    path = f"/activities/{_quote(activity)}/signup"
    r = client.post(path, params={"email": existing})
    assert r.status_code == 400


def test_signup_nonexistent_activity_returns_404(client):
    activity = "No Such Activity"
    path = f"/activities/{_quote(activity)}/signup"
    r = client.post(path, params={"email": "x@a.com"})
    assert r.status_code == 404


def test_unregister_student(client):
    activity = "Basketball Team"
    email = "alex@mergington.edu"
    path = f"/activities/{_quote(activity)}/unregister"
    r = client.post(path, params={"email": email})
    assert r.status_code == 200
    r2 = client.get("/activities")
    assert email not in r2.json()[activity]["participants"]


def test_unregister_not_registered_returns_400(client):
    activity = "Basketball Team"
    email = "notregistered@mergington.edu"
    path = f"/activities/{_quote(activity)}/unregister"
    r = client.post(path, params={"email": email})
    assert r.status_code == 400


def test_unregister_nonexistent_activity_returns_404(client):
    activity = "No Such Activity"
    path = f"/activities/{_quote(activity)}/unregister"
    r = client.post(path, params={"email": "x@a.com"})
    assert r.status_code == 404
