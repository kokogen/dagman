import asyncio
from db.repo import RepoDag, RepoNode, init_tables
import db.sessions
import db.models
import dto
from api.handlers import app
import uvicorn
from config import get_settings


async def main():
    settings = get_settings()
    print('dagman started.')
    
    # Инициализация базы данных
    await init_tables()
    print('Database initialized.')
    
    # Запуск FastAPI приложения
    config = uvicorn.Config(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
    server = uvicorn.Server(config)
    await server.serve()
    
    print('dagman finished')
    
if __name__ == '__main__':
    asyncio.run(main())
        