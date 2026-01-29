from flaskr.db import get_db

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>" in response.data
    

def login(client):
    client.post("/auth/register", data={"username": "u", "password": "p"})
    client.post("/auth/login", data={"username": "u", "password": "p"})



def test_create_post(client):
    login(client)
    response = client.post(
        "/create", 
        data={"title": "Test Post", "body": "Hello Wolr"},
        follow_redirects=True,
    )
    
    assert response.status_code == 200
    assert b"Test Post" in response.data

# Edit Post
def test_edit_post(client, app): 
    login(client)

    client.post(
        "/create",
        data={"title": "Test Post", "body": "Hello World"}
    )

    # Get post id
    with app.app_context():
        db = get_db()
        post_id = db.execute("SELECT id FROM post").fetchone()["id"]


    response = client.post(
        f"/{post_id}/update", 
        data={"title": "Test Edit", "body": "Testing flaskr application"},
        follow_redirects=True,
    )
    assert b"Test Edit" in response.data

# Delete Post
def test_delete_post(client, app):
    login(client)

    client.post(
        "/create",
        data={"title": "Delete Test", "body": "Hello World"},
        follow_redirects=True,
    )
    with app.app_context():
        db = get_db()
        post_id = db.execute("SELECT id FROM post").fetchone()["id"]

    response = client.post(
        f"/{post_id}/delete",
        follow_redirects=True,
    )
    assert b"Delete Test" not in response.data

# Testing user create and submitting empty form
def test_create_post_requires_title(client):
    login(client)

    response = client.post(
        "/create",
        data={"title": "", "body": "No title"},
        follow_redirects=True,
    )
    assert b"Title is required." in response.data

# Testing user update requires titlt
def test_update_post_requires_title(client, app):
    login(client)

    client.post("/create", data={"title": "X", "body": "Y"})

    with app.app_context():
        db = get_db()
        post_id = db.execute("SELECT id FROM post").fetchone()["id"]

    response = client.post(
        f"/{post_id}/update",
        data={"title": "", "body": "Broken"},
        follow_redirects=True,
    )
    assert b"Title is required." in response.data



def test_delete_requires_post(client):
    response = client.get("/1/delete")
    assert response.status_code == 405

# Test 404 
def test_get_post_404(client):
    login(client)
    response = client.post("/2/delete")
    assert response.status_code == 404

# Test 403
def test_update_port_forbidden(client):
    #User A
    client.post("/auth/register", data={"username": "a", "password": "p"})
    client.post("/auth/login", data={"username": "a", "password": "p"})
    client.post("/create", data={"title": "A post", "body": "x"})

    client.get("/auth/logout")

    # User B
    client.post("/auth/register", data={"username": "b", "password": "p"})
    client.post("/auth/login", data={"username": "b", "password": "p"})

    response = client.post("/1/update")
    assert response.status_code == 403