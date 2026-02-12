import requests

# Login as admin
print("=" * 60)
print("TESTING API ENDPOINTS WITH CURL-LIKE REQUEST")
print("=" * 60)

# Login
print("\n1. Logging in as admin...")
login_response = requests.post(
    'https://kanaka.imcbs.com/api/auth/login/',
    json={'username': 'admin', 'password': 'admin123'}
)
print(f"Login Status: {login_response.status_code}")

if login_response.status_code == 200:
    login_data = login_response.json()
    token = login_data.get('tokens', {}).get('access')
    print(f"Token received: {token[:50]}..." if token else "No token")
    
    # Get files
    print("\n2. Getting all files...")
    headers = {'Authorization': f'Bearer {token}'}
    files_response = requests.get(
        'https://kanaka.imcbs.com/api/files/',
        headers=headers
    )
    print(f"Files Status: {files_response.status_code}")
    print(f"Files Response: {files_response.json()}")
else:
    print(f"Login failed: {login_response.text}")

print("\n" + "=" * 60)
