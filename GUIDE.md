# Notify — Setup Guide

## How it works

Alerts are sent via [ntfy.sh](https://ntfy.sh), a free public notification service.
No server, no tunnel, no installation on the target machine required.

```
Sierra Chart (C++) → notify.py → ntfy.sh → phone app
```

---

## Setup

### 1. Choose a topic name

Pick a long, random string — this is your private channel:

```
forex-alerts-k7x9mq2p
```

Anyone who knows this name can send or receive on it, so don't use something guessable.

### 2. Update the config

Edit `settings/config.json`:

```json
{
    "ntfy_url": "https://ntfy.sh/your-topic-name"
}
```

### 3. Install the ntfy app on your phone

- **Android**: [Play Store](https://play.google.com/store/apps/details?id=io.heckel.ntfy) or [F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy/)
- **iOS**: [App Store](https://apps.apple.com/us/app/ntfy/id1625396347)

Open the app → Add subscription → enter your topic name.

### 4. Test

```bash
python test_connection.py   # verify ntfy.sh is reachable
python notify.py "Test alert from Sierra Chart"
```

Your phone should receive the notification immediately.

---

## Sending an alert from C++

```cpp
system("python notify.py \"EURUSD long triggered\"");
```

Check the exit code: `0` = delivered, `1` = failed.

---

## Files

```
notify/
├── notify.py            ← called from Sierra Chart C++ code
├── test_connection.py   ← run before going live to verify connectivity
└── settings/
    └── config.json      ← put your topic URL here
```
