# TODO: Implement the service container other functionalities (auto-resolve, params, factories, interfaces)

from underpy import Encapsulated

class ServiceContainer:
    def __init__(self):
        if getattr(self.__class__, "_initialized", False):
            raise RuntimeError("ServiceContainer instance already exists. Use get_instance().")
        self._services = {}
        self.__class__._initialized = True

    def register(self, name, service):
        """Register a service."""
        self._services[name] = service

    def get(self, name):
        """Retrieve a service."""
        return self._services.get(name)

    @classmethod
    def get_instance(cls):
        """Access the singleton instance."""
        return cls()