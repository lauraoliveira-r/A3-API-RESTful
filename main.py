from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./produtos.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Aplicação FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens; ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Modelo de Produto para o banco de dados
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    descricao = Column(String)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Modelos Pydantic para validação de dados
class ProdutoBase(BaseModel):
    nome: str
    preco: float
    descricao: str

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        orm_mode = True

# Dependência para gerenciar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints da API
@app.get("/")
def read_root():
    return {"message": "API de Gerenciamento de Produtos"}

@app.get("/produtos/", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()

@app.post("/produtos/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}
