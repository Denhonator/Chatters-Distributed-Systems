from models import Message, Server, engine, session, Base

Base.metadata.create_all(engine)

server_0 = Server("7500", 'denho.hopto.org')
server_1 = Server("7501", 'denho.hopto.org')
server_2 = Server("7502", 'denho.hopto.org')
server_3 = Server("7503", 'denho.hopto.org')

message_1 = Message("7500", "yeah", "teemuTheBear")

session.add(server_0)
session.add(server_1)
session.add(server_2)
session.add(server_3)

session.add(message_1)

session.commit()
session.close()
