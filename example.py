from crud import Crud

host = 'localhost'
user = 'root'
password = ''
database = 'arduino_bd'

crud = Crud(host, user, password, database)

result, error = crud.init_connection()
print(f"Conexión establecida: Resultado {result} - Error: {error}")


# Insert a new componente
id_componente, error = crud.insert_componente(
    "actuador", "servomotor", "descripcion del servomotor")

print(f"Componente insertado: {id_componente}")

# Insert a new registro (supposing we have previously inserted a componente with the id 'inserted_componente_id')
id_registro, error = crud.insert_registro(id_componente, 90)
print(f"Componente insertado: {id_registro}")

# Select registros

registros, error = crud.select_registros()
print(error)
print(registros)


# Select componentes
componentes, error = crud.select_componentes()
print(error)
print(componentes)
