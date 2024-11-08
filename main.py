from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users
from app.database.database import engine, Base
from app.routes import books

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookStore API",
    description="""
    API para la tienda de libros
    
    ## Autenticación
    
    ### Endpoints públicos:
    - POST /api/register - Registro de nuevos usuarios
    - POST /api/login - Inicio de sesión
    
    ### Endpoints protegidos:
    Todos los demás endpoints requieren autenticación mediante token Bearer.
    """,
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(
    users.router,
    prefix="/api",
    tags=["Users"]
)

app.include_router(
    books.router,
    prefix="/api/v1",
    tags=["Books"]
)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Bookstore API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )