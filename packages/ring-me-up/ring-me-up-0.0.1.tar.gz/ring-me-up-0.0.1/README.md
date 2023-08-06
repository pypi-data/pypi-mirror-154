# RingMeUp

Send an alarm to your iPhone to ring you up from a failed script when you are asleep.

## Install

`pip install ring-me-up`

## Usage

Set env variables of `icloud_id` & `icloud_password`.

Then:

```
ring
```

Or

```
ring serve [port]
```

to start a server accepting `get`s to ring.
