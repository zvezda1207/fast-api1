# import asyncio
# from .models import init_orm
# from .config import *

# asyncio.run(init_orm())

import asyncio
from models import init_orm
from config import *

asyncio.run(init_orm())
print("Инициализация базы данных завершена.")