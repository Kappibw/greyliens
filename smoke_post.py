# Smoke test script that verifies the forum's guest login,
# message sending, and homepage loading functionality.
import sys
try:
    import requests
except Exception as e:
    print("Missing 'requests' library:", e)
    print("Install with: pip install requests")
    sys.exit(2)

from requests import Session

BASE = "http://127.0.0.1:5000"

def main():
    s = Session()
    try:
        r = s.get(f"{BASE}/guest-login", allow_redirects=True, timeout=5)
        print("GET /guest-login ->", r.status_code)
        print(r.text[:400])
    except Exception as e:
        print("Error during guest-login:", e)

    try:
        r2 = s.post(f"{BASE}/send", data={"content": "Automated test message"}, allow_redirects=True, timeout=5)
        print("POST /send ->", r2.status_code)
        print(r2.text[:400])
    except Exception as e:
        print("Error during POST /send:", e)

    try:
        r3 = s.get(f"{BASE}/", timeout=5)
        print("GET / ->", r3.status_code)
        print(r3.text[:400])
    except Exception as e:
        print("Error during GET /:", e)

if __name__ == '__main__':
    main()
