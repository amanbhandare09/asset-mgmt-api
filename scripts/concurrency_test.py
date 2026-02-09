import requests
import threading
import time

BASE_URL = "http://127.0.0.1:5000"

ASSET_ID = 1
NUM_USERS = 10   # Increase to 50 or 100 for stress test

tokens = []


# -------------------------
# Helper → Register + Login
# -------------------------
def create_user_and_login(index):

    email = f"user{index}@test.com"
    password = "123456"

    # Register
    requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": email,
            "password": password
        }
    )

    # Login
    res = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    token = res.json().get("access_token")

    tokens.append(token)


# -------------------------
# Claim Attempt
# -------------------------
def claim_asset(token, index):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.post(
        f"{BASE_URL}/cashback/{ASSET_ID}/claim",
        headers=headers
    )

    print(f"User {index} → {res.status_code} → {res.json()}")


# -------------------------
# Main Test Runner
# -------------------------
def run_test():

    print("\nCreating users + logging in...\n")

    # Step 1 → Create users
    for i in range(NUM_USERS):
        create_user_and_login(i)

    print("Users ready. Starting concurrent claims...\n")

    threads = []

    # Step 2 → Fire concurrent claims
    for i in range(NUM_USERS):

        t = threading.Thread(
            target=claim_asset,
            args=(tokens[i], i)
        )

        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    print("\nTest completed.")


if __name__ == "__main__":
    time.sleep(1)   # Small delay before start
    run_test()
