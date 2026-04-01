def test_courses_api_requires_login(client):
    response = client.get("/api/courses")
    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Authentication required."


def test_get_courses(auth_client):
    response = auth_client.get("/api/courses")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] >= 1


def test_get_course_by_id(auth_client):
    courses_response = auth_client.get("/api/courses")
    course_id = courses_response.get_json()["data"][0]["id"]

    response = auth_client.get(f"/api/courses/{course_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "name" in data["data"]
    assert "code" in data["data"]


def test_get_course_not_found(auth_client):
    response = auth_client.get("/api/courses/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Course not found."


def test_create_course(auth_client):
    response = auth_client.post(
        "/api/courses",
        json={
            "name": "Image Processing",
            "code": "CPE450",
            "description": "Digital image analysis",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["data"]["code"] == "CPE450"


def test_create_course_missing_fields(auth_client):
    response = auth_client.post(
        "/api/courses",
        json={"name": "Only Name"},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required fields" in data["error"]


def test_create_course_invalid_code(auth_client):
    response = auth_client.post(
        "/api/courses",
        json={
            "name": "Image Processing",
            "code": "CPE@450",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Course code must contain only letters, numbers, or dashes."


def test_create_course_duplicate_name(auth_client):
    response = auth_client.post(
        "/api/courses",
        json={
            "name": "Data Structures",
            "code": "NEW101",
            "description": "Another course",
        },
    )
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Course name already exists."


def test_create_course_duplicate_code(auth_client):
    response = auth_client.post(
        "/api/courses",
        json={
            "name": "Another Data Structures",
            "code": "CSE201",
            "description": "Another course",
        },
    )
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Course code already exists."


def test_update_course(auth_client):
    create_response = auth_client.post(
        "/api/courses",
        json={
            "name": "Signals and Systems",
            "code": "CPE340",
            "description": "Signals basics",
        },
    )
    course_id = create_response.get_json()["data"]["id"]

    response = auth_client.put(
        f"/api/courses/{course_id}",
        json={
            "description": "Updated description",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["description"] == "Updated description"


def test_update_course_name_and_code(auth_client):
    create_response = auth_client.post(
        "/api/courses",
        json={
            "name": "Old Course",
            "code": "OLD101",
            "description": "Old description",
        },
    )
    course_id = create_response.get_json()["data"]["id"]

    response = auth_client.put(
        f"/api/courses/{course_id}",
        json={
            "name": "New Course",
            "code": "NEW101",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["name"] == "New Course"
    assert data["data"]["code"] == "NEW101"


def test_update_course_not_found(auth_client):
    response = auth_client.put(
        "/api/courses/99999",
        json={"description": "Updated"},
    )
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Course not found."


def test_update_course_duplicate_name(auth_client):
    auth_client.post(
        "/api/courses",
        json={
            "name": "Course One",
            "code": "ONE101",
            "description": "desc",
        },
    )
    create_response = auth_client.post(
        "/api/courses",
        json={
            "name": "Course Two",
            "code": "TWO101",
            "description": "desc",
        },
    )
    course_id = create_response.get_json()["data"]["id"]

    response = auth_client.put(
        f"/api/courses/{course_id}",
        json={"name": "Course One"},
    )
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Course name already exists."


def test_update_course_duplicate_code(auth_client):
    auth_client.post(
        "/api/courses",
        json={
            "name": "Course A",
            "code": "AAA101",
            "description": "desc",
        },
    )
    create_response = auth_client.post(
        "/api/courses",
        json={
            "name": "Course B",
            "code": "BBB101",
            "description": "desc",
        },
    )
    course_id = create_response.get_json()["data"]["id"]

    response = auth_client.put(
        f"/api/courses/{course_id}",
        json={"code": "AAA101"},
    )
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Course code already exists."


def test_delete_course(auth_client):
    create_response = auth_client.post(
        "/api/courses",
        json={
            "name": "Microprocessors",
            "code": "CPE330",
            "description": "Processor systems",
        },
    )
    course_id = create_response.get_json()["data"]["id"]

    response = auth_client.delete(f"/api/courses/{course_id}")
    assert response.status_code == 204


def test_delete_course_not_found(auth_client):
    response = auth_client.delete("/api/courses/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Course not found."


def test_invalid_json_body_on_course_post(auth_client):
    response = auth_client.post(
        "/api/courses",
        data="not-json",
        content_type="text/plain",
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Request body must be valid JSON."


def test_invalid_json_body_on_course_put(auth_client):
    response = auth_client.put(
        "/api/courses/1",
        data="not-json",
        content_type="text/plain",
    )
    assert response.status_code in [400, 404]
