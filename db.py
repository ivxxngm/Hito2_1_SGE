import mysql.connector
from mysql.connector import Error

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='encuestas',
            user='root',
            password='curso'
        )
        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
            return conn
    except Error as e:
        print(f"Error en la conexión: {e}")
        return None

def agregar_encuesta(id_encuesta, edad, sexo, bebidas_semana, cervezas_semana,
                    bebidas_fin_semana, bebidas_destiladas, vinos_semana,
                    perdidas_control, diversion_dependencia, problemas_digestivos,
                    tension_alta, dolor_cabeza):
    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        # Consulta SQL
        query = """
        INSERT INTO ENCUESTA (
            idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana,
            BebidasFinSemana, BebidasDestiladasSemana, VinosSemana,
            PerdidasControl, DiversionDependenciaAlcohol,
            ProblemasDigestivos, TensionAlta, DolorCabeza
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Crear tupla con valores
        valores = (
            id_encuesta,
            edad,
            sexo,
            bebidas_semana,
            cervezas_semana,
            bebidas_fin_semana,
            bebidas_destiladas,
            vinos_semana,
            perdidas_control,
            diversion_dependencia,
            problemas_digestivos,
            tension_alta,
            dolor_cabeza
        )
        
        cursor.execute(query, valores)
        conn.commit()
        return True

    except Exception as e:
        print(f"Error al agregar la encuesta: {e}")
        raise Exception(f"Error al agregar la encuesta: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def leer_encuesta(id_encuesta):
    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        # Consulta SQL
        query = """
        SELECT * FROM ENCUESTA 
        WHERE idEncuesta = %s
        """
        
        cursor.execute(query, (id_encuesta,))
        resultado = cursor.fetchone()
        
        return resultado

    except Exception as e:
        print(f"Error al leer la encuesta: {e}")
        raise Exception(f"Error al leer la encuesta: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def editar_encuesta(id_encuesta, edad, sexo, bebidas_semana, cervezas_semana,
                    bebidas_fin_semana, bebidas_destiladas, vinos_semana,
                    perdidas_control, diversion_dependencia, problemas_digestivos,
                    tension_alta, dolor_cabeza):
    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        query = """
        UPDATE ENCUESTA 
        SET edad = %s,
            Sexo = %s,
            BebidasSemana = %s,
            CervezasSemana = %s,
            BebidasFinSemana = %s,
            BebidasDestiladasSemana = %s,
            VinosSemana = %s,
            PerdidasControl = %s,
            DiversionDependenciaAlcohol = %s,
            ProblemasDigestivos = %s,
            TensionAlta = %s,
            DolorCabeza = %s
        WHERE idEncuesta = %s
        """
        
        valores = (
            edad,
            sexo,
            bebidas_semana,
            cervezas_semana,
            bebidas_fin_semana,
            bebidas_destiladas,
            vinos_semana,
            perdidas_control,
            diversion_dependencia,
            problemas_digestivos,
            tension_alta,
            dolor_cabeza,
            id_encuesta  # El ID va al final porque es el WHERE
        )
        
        cursor.execute(query, valores)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise Exception("No se encontró la encuesta para editar")
            
        return True

    except Exception as e:
        print(f"Error al editar la encuesta: {e}")
        raise Exception(f"Error al editar la encuesta: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def eliminar_encuesta(id):
    conn = conectar_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM encuestas WHERE id=%s"
            valor = (id,)
            cursor.execute(sql, valor)
            conn.commit()
            print("Encuesta eliminada exitosamente")
        except Error as e:
            print(f"Error al eliminar encuesta: {e}")
        finally:
            cursor.close()
            conn.close()