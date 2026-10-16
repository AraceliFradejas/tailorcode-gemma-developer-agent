"""Exercise the server's metrics/HTTP integration on CPU without loading a model."""
from importlib.metadata import version


def main():
    from fastapi import APIRouter, FastAPI
    from fastapi.testclient import TestClient
    from prometheus_fastapi_instrumentator import Instrumentator

    app = FastAPI()
    router = APIRouter()

    @router.get('/health')
    def health():
        return {'status': 'ok'}

    app.include_router(router)
    Instrumentator().instrument(app).expose(app)
    with TestClient(app) as client:
        for path in ('/health', '/metrics'):
            response = client.get(path)
            if response.status_code != 200:
                raise RuntimeError(f'{path}: HTTP {response.status_code}')
        if client.get('/health').json() != {'status': 'ok'}:
            raise RuntimeError('Unexpected health response')
    for package in ('fastapi', 'starlette', 'prometheus-fastapi-instrumentator'):
        print(f'{package}: {version(package)}')
    print('HTTP and metrics checks passed on CPU. No model loaded.')


if __name__ == '__main__':
    main()
