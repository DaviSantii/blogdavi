from blogdavi import app, database
from blogdavi.models import Usuario, Post

# Criar o banco de dados
#with app.app_context():
#    database.create_all()

# Deletar o banco de dados e criar dnv
with app.app_context():
   database.drop_all()
   database.create_all()

#usuario = Usuario(username='Davi', email='davi.santiago.6@gmail.com', senha='123456')
#usuario2 = Usuario(username='Nathan', email='zorcerocha@gmail.com', senha='123456')

# Adição de dados no banco de dados
# with app.app_context():
#     database.session.add(usuario)
#     database.session.add(usuario2)

#     database.session.commit()

# Pegar todos os usuarios, buscar o primeiro do banco de dados 
# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     primeiro = Usuario.query.first()
#     print(primeiro.posts)# Tem que buscar aqui pois ele usa uma função do tipo database(relationship)
# print(primeiro.id)
# print(primeiro.username)
# print(primeiro.email)
# print(primeiro.senha)

# Pegar apenas o primeiro usuario com id=2(ou todos)
# with app.app_context():
#     usuario_teste = Usuario.query.filter_by(id=2).first()#.all()
#     print(usuario_teste.posts)
# print(usuario_teste.id)
# print(usuario_teste.username)
# print(usuario_teste.email)

# Coluna autor do post gerada pela chave estrangeira
# with app.app_context():
#     post = Post.query.first()
#     print(post.titulo)
#     print(post.autor.username)