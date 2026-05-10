import requests
import sys
import json
import traceback
from pathlib import Path

CONFIG = Path(__file__).parent / "settings" / "config.json"
TIMEOUT = 5


def load_health_url() -> str:
    with open(CONFIG) as f:
        base = json.load(f)["ntfy_url"]
    # Strip topic segment and append health endpoint
    root = "/".join(base.split("/")[:3])
    return f"{root}/v1/health"


NTFY_HEALTH_URL = load_health_url()


def test_connection() -> bool:
    print(f"[INFO] Testing connection to: {NTFY_HEALTH_URL}")
    print(f"[INFO] Timeout: {TIMEOUT}s\n")

    try:
        r = requests.get(NTFY_HEALTH_URL, timeout=TIMEOUT)

        print(f"[INFO] HTTP status code : {r.status_code}")
        print(f"[INFO] Response headers : {dict(r.headers)}")
        print(f"[INFO] Raw response body: {r.text}")

        if r.status_code != 200:
            print(f"\n[FAIL] Server returned non-200 status: {r.status_code}")
            print(f"       Expected 200. ntfy may be down or misconfigured.")
            return False

        try:
            body = r.json()
        except json.JSONDecodeError as e:
            print(f"\n[FAIL] Response was not valid JSON.")
            print(f"       JSON parse error: {e}")
            print(f"       Raw body was: {r.text!r}")
            return False

        healthy = body.get("healthy")

        if healthy is not True:
            print(f"\n[FAIL] ntfy reports unhealthy.")
            print(f"       'healthy' field value: {healthy!r}")
            print(f"       Full response: {body}")
            return False

        print("\n[OK] ntfy is healthy and reachable.")
        return True

    except requests.exceptions.ConnectionError as e:
        print("[FAIL] Connection error — could not reach ntfy.sh.")
        print(f"       Check your internet connection.")
        print(f"       Detail: {e}")
        return False

    except requests.exceptions.Timeout:
        print(f"[FAIL] Request timed out after {TIMEOUT}s.")
        print(f"       ntfy.sh is not responding — the service may be temporarily down.")
        return False

    except requests.exceptions.TooManyRedirects as e:
        print("[FAIL] Too many redirects.")
        print(f"       ntfy_url in config.json may be malformed.")
        print(f"       Detail: {e}")
        return False

    except requests.exceptions.SSLError as e:
        print("[FAIL] SSL certificate error.")
        print(f"       The tunnel domain may have an invalid or expired certificate.")
        print(f"       Detail: {e}")
        return False

    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Unexpected requests error: {type(e).__name__}")
        print(f"       Detail: {e}")
        return False

    except Exception:
        print("[FAIL] Unhandled exception during connection test:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
