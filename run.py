from app import create_app
from config import settings


if __name__ == '__main__':
    create_app().run(port=settings.PORT, debug=True)
