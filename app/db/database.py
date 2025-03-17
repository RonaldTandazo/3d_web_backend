from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import MONGO_URI, PGSQL_URL

# 🔹 Conexión a MongoDB
# mongo_client = AsyncIOMotorClient(MONGO_URI)
# mongo_db = mongo_client.get_database()  # Cambia esto por el nombre de tu base de datos

# 🔹 Conexión a PostgreSQL con SQLAlchemy
engine = create_async_engine(PGSQL_URL, future=True, echo=True)

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependencia para obtener la sesión de PostgreSQL
async def get_db():
    async with SessionLocal() as session:
        yield session