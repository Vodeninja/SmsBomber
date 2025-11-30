from utils.service_loader import load_services

_services = load_services()
__all__ = [s.__name__ for s in _services]

def get_all_services():
    return _services.copy()

