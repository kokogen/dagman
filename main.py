import asyncio
import db.repo
import db.sessions

async def main():
    await db.repo.init_tables()
    print('dagman started.')
    print('dagman finished')
    

if __name__ == '__main__':
    print(db.sessions.url_object)
    #asyncio.run(main())
        