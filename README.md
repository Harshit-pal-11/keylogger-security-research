# Keylogger Security Research

A transparent, local-only keyboard event demo for an internship or classroom lab. It illustrates event-driven input handling and JSON Lines logging inside a dedicated application window.

## Safety and scope

This demo captures key events only when all of the following are true:

- The user starts recording through the visible button and confirms the prompt.
- The user types in this application's text box while the application has focus.

It does not monitor other applications, run in the background, hide itself, start automatically, or transmit data over a network. Use synthetic text only. Do not enter passwords, personal information, or other real secrets. Run it only on a device you own or are authorized to use.

## Requirements

- Python 3
- Tkinter (included with most standard Python installations; some Linux distributions package it separately)

No third-party Python packages are required.

## Run

```bash
python user.py
```

Click the text area and enter dummy text. Select **Start recording** and confirm to begin. Select **Stop recording** to end the session. A visible status label shows whether recording is active and where the local log is stored.

## Log format

Each key press is written as one JSON object per line, with a UTC timestamp, Tk key symbol, and character value. Logs are created in `logs/` beside the script. They remain on the machine and are excluded from Git by `.gitignore`.

## Project structure

```text
keylogger-security-research/
├── .gitignore
├── README.md
└── user.py
```

## Learning goals

- Bind and handle keyboard events in a focused GUI widget.
- Add explicit user-controlled start and stop behavior.
- Write structured event records in JSON Lines format.
- Discuss privacy, consent, data minimization, and defensive monitoring.

## Limitations

This is a teaching demo, not an endpoint monitoring or security product. It intentionally has no global keyboard hook, persistence, stealth, privilege escalation, or network transport.
