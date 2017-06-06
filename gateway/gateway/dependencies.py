from nameko.extensions import DependencyProvider


class Config(DependencyProvider):

    def get_dependency(self, worker_ctx):
        return self.container.config.copy()
