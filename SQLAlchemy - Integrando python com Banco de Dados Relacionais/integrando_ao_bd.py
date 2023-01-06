from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect, select, func

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_name = Column(String)

    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.full_name})"

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"

# Conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    miguel = User(
        name='Miguel',
        full_name='Miguel Kawakami',
        address=[Address(email_address='migskawakami@gmail.com'),
                 Address(email_address='m.kawakami@aluno.ifsp.edu.br')]
    )

    arthur = User(
        name='Arthur',
        full_name='Arthur Cruciari',
        address=[Address(email_address='arthur.cruciari@gmail.com')]
    )

    patrick = User(
        name='Patrick',
        full_name='Patrick Estrela'
    )
    # Enviando para o BD (persistência de dados)
    session.add_all([miguel, arthur, patrick])
    session.commit()

stmt = select(User).where(User.name.in_(['Miguel', 'Arthur']))
print("\nRecuperando usuários a partir de condição de filtragem")
for user in session.scalars(stmt):
    print(user)

print("\nRecuperando os endereços de email de Miguel (id=1)")
stmt_address = select(Address).where(Address.user_id.in_([1]))
for address in session.scalars(stmt_address):
    print(address)

stmt_order = select(User).order_by(User.full_name)
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)


stmt_join = select(User.full_name, Address.email_address).join_from(Address, User)
print("\n")
for result in session.scalars(stmt_address):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

print("\nTotal de instâncias em user")
stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)