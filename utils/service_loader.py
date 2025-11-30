import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import List, Type
from core.base_service import BaseService


def load_services(services_package: str = 'services') -> List[Type[BaseService]]:
    services = []
    package_path = Path(services_package)
    
    if not package_path.exists():
        package_path = Path(__file__).parent.parent / services_package
    
    package = importlib.import_module(services_package)
    
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if ispkg:
            continue
        
        try:
            module = importlib.import_module(modname)
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (obj != BaseService and 
                    issubclass(obj, BaseService) and 
                    obj.__module__ == modname):
                    services.append(obj)
        except Exception:
            continue
    
    return services

