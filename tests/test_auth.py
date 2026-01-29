# ================= REGISTRATION =======================
# Test Registration
def test_register(client):
    response = client.post(
        "/auth/register",
        data={"username": "test", "password": "test123"},
        follow_redirects=True,
    )
    assert b"Log In" in response.data

# Test for missing username and password in register
def test_register_missing_username(client):
    response = client.post(
        "/auth/register",
        data={"username": "", "password": "test123"},
        follow_redirects=True,
    )
    assert b"Username is required." in response.data

def test_register_missing_password(client):
    response = client.post(
        "/auth/register",
        data={"username": "test2", "password": ""},
        follow_redirects=True,
    )
    assert b"Password is required." in response.data


# Test for duplicate registration username and password
def test_register_duplicate(client):
    client.post(
        "/auth/register",
        data={"username": "test3", "password": "pass"},
        follow_redirects=True,
    )
    response = client.post(
        "/auth/register",
        data={"username": "test3", "password": "pass"},
        follow_redirects=True,
    )
    assert b"already registered" in response.data


#======================  LOG IN =================
# Test Login after registration
def test_login(client):
    client.post(
        "/auth/register",
        data={"username": "test", "password": "test123"},
        follow_redirects=True,
    )

    response = client.post(
        "/auth/login",
        data={"username": "test", "password": "test123"},
        follow_redirects=True,
    )

    assert b"Log Out" in response.data
    #print(response.data.decode)

# This confirms unauthorized users are blocked
def test_create_requires_login(client):
    response = client.post("/create")
    assert response.status_code == 302
    assert "auth/login" in response.headers["Location"]

# Test login errors
def test_login_wrong_username(client):
    response = client.post(
        "/auth/login",
        data={"username": "wrong", "password": "test"},
        follow_redirects=True
    )
    assert b"Incorrect username." in response.data

def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        data={"username": "test4", "password": "test123"},
        follow_redirects=True
    )
    response = client.post(
        "/auth/login",
        data={"username": "test4", "password": "wrong"},
        follow_redirects=True
    )
    assert b"Incorrect password." in response.data


# =========== GET REQUEST =======================
def test_register_get(client):
    response = client.get("/auth/register")
    assert b"Register" in response.data

def test_login_get(client):
    response = client.get("/auth/login")
    assert b"Log In" in response.data


# ================= LOG OUT ========================
def test_logout(client):
    client.post(
        "auth/register",
        data={"username": "test5", "password": "test12345"},
        follow_redirects=True,
    )
    client.post(
        "auth/login",
        data={"username": "test5", "password": "test12345"},
        follow_redirects=True,
    )
    response = client.get(
        "/auth/logout",
        follow_redirects=True,
    )
    assert b"Log In" in response.data # confirms session cleared
    print(response.data.decode)