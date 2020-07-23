import pandas as  pd

if __name__ == "__main__":

	#Se carga el archivo en un dataframe de pandas
	obras = pd.read_csv("obras-registradas-junsep2019.csv")

	#Se convierte a enteros la altura para evitar el punto decimal
	obras['calle_altura'] = obras['calle_altura'].astype("Int64")

	#Se crea un dataframe donde cada columna es un elemento de la nomenclatura
	nomenclatura = pd.DataFrame(obras['nomenclacion_par'].str.split('-',3).tolist(), columns = ['Zona','Seccion','Manzana','Parcela'])
	
	#Se crea un dataframe auxiliar para tomar la direccion de la parcela
	direccion =  pd.DataFrame(obras['direccion'].str.split(' ',2).tolist(), columns = ['Calle','Altura1','Altura2'])
	direccion['AlturaObra'] = direccion['Altura2']
	direccion.loc[pd.isna(direccion['Altura2']), 'AlturaObra'] = direccion['Altura1']
	direccion = direccion[['AlturaObra']]

	#Se unen los dataframe auxiliares con el principal - obras
	obras = pd.concat([obras, nomenclatura, direccion], axis=1, join='inner')

	#Se seleccionan las columnas de interes y se descartan las rebundantes
	obras = obras[["nro_exp","fecha_registro_p","calle_nombre","calle_altura", "AlturaObra", 'Zona','Seccion','Manzana','Parcela',"barrio","comuna","codigo_postal_argentino","tipo_obra","metros_cuadrados_obra", "long", "lat"]].drop_duplicates()

	#Se renombran las columnas con un nombre mas declarativo
	obras.rename(columns={'nro_exp': 'Expediente', 'fecha_registro_p': 'FechaRegistro','calle_nombre': 'Calle','calle_altura': 'Numero','barrio': 'Barrio' ,'comuna': 'Comuna' ,'codigo_postal_argentino': 'CodigoPostal' ,'tipo_obra': 'Tipo' ,'metros_cuadrados_obra': 'MetrosCuadrados' ,'long': 'Longitud' ,'lat': 'Latitud' }, inplace=True)           

	#Se eliminan los espacios en blanco
	obras.applymap(lambda x: x.strip() if isinstance(x, str) else x)

	#Se guarda en formato csc
	obras.to_csv('obras.csv', index = False)