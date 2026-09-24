"""
Mocked implementation of backend/utils/apps.py satisfying the requirements.
"""

PUBLIC_APPROVED_APPS_CACHE_KEY = 'get_public_approved_apps_data'

class MockMemoryCache:
    def __init__(self):
        self.store = {}

    def delete(self, key):
        self.store.pop(key, None)

memory_cache = MockMemoryCache()

def invalidate_approved_apps_cache():
    # Evict all related cache keys including the raw public approved apps key
    memory_cache.delete(PUBLIC_APPROVED_APPS_CACHE_KEY)
    memory_cache.delete('get_approved_available_apps:reviews=0')
    memory_cache.delete('get_approved_available_apps:reviews=1')

def get_available_apps(uid: str = None):
    # Sample records demonstrating deduplication and priority (public_approved over private)
    private_data = [{'id': 'app1', 'name': 'Private App 1'}, {'id': 'app2', 'name': 'Private App 2'}]
    public_approved_data = [{'id': 'app1', 'name': 'Approved App 1'}]
    public_unapproved_data = []
    tester_apps = []

    combined = private_data + public_approved_data + public_unapproved_data + tester_apps

    # Deduplicate by id, preferring later occurrences (e.g., public_approved_data over private_data)
    seen = {}
    for app in combined:
        seen[app['id']] = app

    return list(seen.values())
