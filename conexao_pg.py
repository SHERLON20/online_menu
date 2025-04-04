import pg8000

conn = pg8000.connect(
    database= 'pedidos_t8nl',
    user= 'pedidos_t8nl_user',
    password='ncLLceD4sGaRYm0J6Fi65pcoK0ZJWl2P',
    host= 'dpg-cvmpknhr0fns73akf2c0-a.oregon-postgres.render.com',
    port = '5432',
)

if conn:
    print('conectado com sucesso')