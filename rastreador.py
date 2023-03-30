import math

#-- Tracker class
class Rastreador:
    #-Inicializamos variables
    def __init__(self):
        #Aqui almacenamos las posiciones centrales
        self.centroPuntos= {}
        #Contador de objetos
        self.idCount= 1

    def rastreo(self, objetos):
        #Almacenamos los objetos identificados
        objetos_id= []

        #Obtenemos el punto central del nuevo objeto
        for rect in objetos:
            x1, y1, x2, y2= rect
            cx= (x1 + x2) // 2
            cy= (y1 + y2) // 2
            #print(f"Antes del for, cx= {cx} y cy= {cy}")

            #Verificamos si el objeto ya fue detectado
            objecto_det= False
            for id, pt in self.centroPuntos.items():
                dist= math.hypot(cx - pt[0], cy - pt[1]) #Verificamos la proximidad calculando la longitud del vector

                if dist < 70:
                    self.centroPuntos[id]= (cx, cy)  #Actualizamos el punto central
                    print(self.centroPuntos)
                    objetos_id.append([x1,y1,x2,y2, id]) #Enviamos de vuelta el bbox con el id identificado
                    #print(objetos_id)
                    objecto_det= True
                    break
            
            #Si detecta un nuevo objeto le asignamos el id a ese objeto
            if objecto_det is False:
                self.centroPuntos[self.idCount]= (cx, cy) #Almacenamos las coordenadas
                objetos_id.append([x1, y1, x2, y2, self.idCount]) #Agregamos el objeto con su id
                self.idCount= self.idCount + 1            #Aumentamos el id
            
        # Limpiar la lista de puntos centrales para eliminar los ids que ya no se usen
        new_center_points= {}
        for obj_by_id in objetos_id:
            _, _, _, _, object_id= obj_by_id
            center= self.centroPuntos[object_id]
            new_center_points[object_id]= center

        #Acturalizamos la lista con los id no utilizados eliminados
        self.centroPuntos= new_center_points.copy()
        return objetos_id