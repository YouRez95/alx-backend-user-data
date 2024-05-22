#!/usr/bin/env python3
""" Main 5
"""

from api.v1.auth.auth import Auth


test = Auth()

print(test.require_auth('/api/v1/users', ["/api/v1/stat*"]))
print(test.require_auth('/api/v1/status', ["/api/v1/stat*"]))
print(test.require_auth('/api/v1/stats', ["/api/v1/stat*"]))
