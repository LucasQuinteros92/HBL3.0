
import json



def agregarComentario(contenido, lista :list ):
    if contenido != "":
        lista.append(f"#######{contenido}######\n")
    return lista

def agregarVariable(contenido,key,nivel,lista : list,nombreModulo = ""):
    if nombreModulo != "":
        nombreModulo += "_"
    tabs = "\t"*nivel

    if isinstance(contenido,str):
        lista.append(f"{tabs}{key} = '{contenido}'")
    else:
        lista.append(f"{tabs}{key} = {contenido}")
    
    return lista
def agregarClase(contenido,nivel, lista :list ):

    tabs = "\t"*(nivel)    
    if nivel == 1:
        lista.append(f"{tabs}class {contenido}():\n")
        tabs = "\t"*(nivel+1) 
        lista.append(f"{tabs}name = '{contenido}'\n")
    else:
        lista.append(f"{tabs}class {contenido}cfg():\n")
        
    
def leerDiccionario(dicc : dict,_nombreModulo = "",_nivel = 0,lista :list = []):
    
    for key in dicc.keys():
        content = dicc.get(key)
        if _nivel == 0:
            agregarComentario(key.upper(),lista)
            
        if isinstance(content,dict):
            #agregarComentario(f"{key.upper()}",lista)
            agregarClase(f"{key.capitalize()}",_nivel,lista)
            leerDiccionario(content,key,_nivel + 1,lista) 
            
        else:
            
            agregarVariable(content,key,_nivel,lista,_nombreModulo)
            
        lista.append("\n")
        
    return lista

def leerConfig(modulo = ""):
    with open("configuracion/configHBL.json","r") as fp:
        config :dict= json.load(fp)
        
    #print(config)
    
    return leerDiccionario(config,modulo)
    

def guardarVariables(lineas):
    with open("configuracion/Settings.py","w") as fp:
        fp.writelines(f"#ADVERTENCIA:\n#ESTE ARCHIVO SE GENERA DINAMICAMENTE\n#NO MODIFICAR\n\n")
        fp.writelines(lineas)
        
def generarConfiguracion():
    
    guardarVariables(leerConfig())


generarConfiguracion()
    