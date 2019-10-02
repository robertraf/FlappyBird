import random
import time

def setup():
    size(400,708)
    frameRate(30)
    fill(0)
    textSize(48)

    global img,b,a,escena,isIntro,isPlaying,mundo,miDiccionario,misNombres,isGameOver,gamestate,auxi,auxi2,arch,nombrecito
    
    with open('nombre.txt') as file: #Abriendo archivo con el nombre
        nombrecito = file.read()
        
    gamestate = 1
    arch = Puntajes()
    auxi = arch.recuperar_puntajes('puntajes.txt')    
    isIntro = True
    isPlaying = False
    isGameOver = False 
    misNombres = []
    miDiccionario = {}
    escena = Escena()
    mundo = Mundo()
    a = Jugador(width/2-150,height/2,nombrecito)
    a.adicionar()
    b = [] #Aqui se almacenan los obstáculos
    b.append(Obstaculo(width,random.randint(250,600)))
    img = [loadImage('data/0.png'),loadImage('data/1.png'),loadImage('data/2.png'),
           loadImage('data/bottom.png'),loadImage('data/top.png'),loadImage('data/background.png'),
           loadImage('data/dead.png'),loadImage('data/FlappyBird.png'),loadImage('data/Play.png'),
           loadImage('data/Restart.png'),loadImage('data/ScoreTable.png'),loadImage('data/GameOver.png'),
           loadImage('data/New.png'),loadImage('data/ScoreTableIntro.png')]
                           
def draw():
    escena.play()


class Mundo():
    
    def iniciar(self):
        
        if gamestate == 0:
            image(img[5],0,0) #Agregar Background 
            
            if a.vivo:
                for i in range(len(b)):
                    if b[i].getX() + 98 < width - 200 and b[i].getIndicador():
                        b[i].setIndicador(False)
                        b.append(Obstaculo(width,random.randint(250,600)))
                        
                    if b[i].getX() <= width/2 - 150 and b[i].indicadorAumento: #Aumento de puntaje
                        a.aumentarPuntaje()
                        b[i].indicadorAumento = False
                        
            if len(b)>0: #Pintando los tubos
                for i in range(len(b)):
                    b[i].dibujar()
                    
            a.dibujar() #Pintando al pajarito
            textSize(48) #Mostrando el puntaje en pantalla 
            text(a.getPuntaje(),width/2,100)
            
            if keyPressed and key == ' ' and a.vivo: #Evento de la tecla espacio que hace saltar al pajaro
                a.setGravedad(3+a.aumento)
                a.saltar(a.gravedad+16)
                
            else:
                a.aumentarGravedad(1)
                a.caer(a.gravedad)
                
            if a.indicador >= 1: #aumento de velocidad de los tubos
                Obstaculo.velocidad += 1  
                a.indicador = 0
                a.aumento += 1
                
            if len(b)>0 and a.vivo: #Movimiento Tubo
                for i in range(len(b)):
                    b[i].mover()
                        
            for i in range(len(b)): #colisiones con tubos
                if (b[i].getX() < a.getX() < b[i].getX() + 98 or b[i].getX( )< a.getX() + 40 < b[i].getX() + 98):
                    if (b[i].getY() < a.getY( )+ 30 or (a.getY()< b[i].aux + 500)):
                        a.vivo = False  
                              
            if  a.getY() + 30 >= height and a.vivo == True: #Colision abajo
                a.vivo = False
                a.saltar(a.gravedad + 50)
            
            if  a.getY() + 30 <= 0 and a.vivo == True: #Colision arriba
                a.vivo = False
                a.saltar(a.gravedad + 50)
                
            if a.getY() + 30 >= height and a.vivo == False:
                cambiar()
    
    
class Puntajes(): #Persistencia
    
    def guardar_puntajes(self,nombre_archivo,puntajes):
        aux = self.recuperar_puntaje_maximo(nombre_archivo)
        for n in puntajes:
            if aux:
                with open(nombre_archivo,'w') as archivo:
                    archivo.write(n+":"+str(puntajes[n])+"\n")
 
    def recuperar_puntajes(self,nombre_archivo):
        puntajes = []
        with open(nombre_archivo,"r") as archivo:
            for linea in archivo:
                nombre,puntaje = linea.rstrip("\\n").split(":")
                x=puntaje.split(',')
                puntajes.append(nombre)
                puntajes.append(int(x[0]))
                puntajes.append(x[1])
        return puntajes
    
    def recuperar_puntaje_maximo(self,nombre_archivo):
        puntajes = []
        with open(nombre_archivo,"r") as archivo:
            for linea in archivo:
                nombre,puntaje = linea.rstrip("\\n").split(":")
                d = puntaje.split(",")
                x = d[0].split('[')
                puntajes.append(int(x[0]))
        if max(puntajes) > a.getPuntaje():
            return False
        else:
            return True    

def cambiar(): #Cambiar
    global isIntro,isPlaying,isGameOver,gamestate
    isGameOver = True
    isPlaying = False
    isIntro = False
    gamestate = 1
    escena.play()
    

class Escena(): #Clase Escenas
    
    def intro(self):
        global gamestate
        background(0)
        image(img[5],0,0)
        image(img[7],width/2-175,height/2-250)
        fill(0);
        noStroke();
        textSize(20)
        ellipse(width/2,height/2-50,80,80);
        image(img[8],width/2-40,height/2-90)
        image(img[13],width/2-175,400)
        text(auxi[0],width/2-60,480)
        text(auxi[1],width/2-60,510)
        text(auxi[2],width/2-60,540)
                        
    def gameOver(self):
        global auxi,auxi2
        background(0)
        image(img[5],0,0)
        fill(0);
        noStroke();
        ellipse(width/2,height/2-50,80,80);
        image(img[9],width/2-38,height/2-38-50)
        image(img[11],width/2-164,130)
        image(img[10],width/2-175,400)
        textSize(15)
        
        for n in misNombres:
            miDiccionario[n] = str(a.getPuntaje()) + ',' + time.strftime("%d/%m/%y")
                    
        if a.numero == 0:
            auxi2 = [a.nombre,a.puntaje,time.strftime("%d/%m/%y")]
            arch.guardar_puntajes('puntajes.txt',miDiccionario)
            auxi = arch.recuperar_puntajes('puntajes.txt')
            a.numero += 1 
        
        if auxi[1] > a.puntaje: #caso cuando el archivo tiene mejor puntaje
            text(auxi[0],width/2+50,500)
            text(auxi[1],width/2+50,520)
            text(auxi[2],width/2+50,540)
            text(auxi2[0],width/2-120,500)
            text(auxi2[1],width/2-120,520)
            text(auxi2[2],width/2-120,540)
        
        else: #caso cuando batís el record
            image(img[12],width/2+65, 415)
            text(auxi2[0],width/2-120,500)
            text(auxi2[1],width/2+-120,520)
            text(auxi2[2],width/2+-120,540)
            text(auxi2[0],width/2+50,500)
            text(auxi2[1],width/2+50,520)
            text(auxi2[2],width/2+50,540)
            
    def play(self):
        if (isIntro):
            self.intro()
            
        elif (isPlaying):
            mundo.iniciar()
            
        elif (isGameOver):
            self.gameOver()
            
def mousePressed(): #Presionar botonMouse
    global isIntro,isPlaying,isGameOver,gamestate,b
    
    if(isIntro):
        if (mouseX >= width/2 - 40 and mouseX <= width/2 + 40):
            if (mouseY <= height/2 + 10 and mouseY >= height/2 - 90):
                gamestate = 0
                isPlaying = True
                isIntro = False
                isGameOver = False
                escena.play()
                
    elif(isGameOver):
        if (mouseX >= width/2 - 40 and mouseX <= width/2 + 40):
            if (mouseY <= height/2 + 10 and mouseY >= height/2 - 90):
                gamestate = 0
                isPlaying = True
                isIntro = False
                isGameOver = False
                a.vivo = True
                a.indicador = 0
                a.puntaje = 0
                a.gravedad = 3
                a.y = height/2
                a.aumento = 0
                a.numero = 0
                arch = Puntajes()
                b = []
                Obstaculo.velocidad = 10
                b.append(Obstaculo(width,random.randint(250,600)))
                escena.play()
        
        
class Elemento(): #Clase padre
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
                
class Jugador(Elemento): #Clase hijo
        
    def __init__(self,x,y,nombre):
        Elemento.__init__(self,x,y)
        self.nombre = nombre
        self.gravedad = 10
        self.velocidadSalto = 10
        self.vivo = True
        self.puntaje = 0
        self.numero = 0
        self.indicador = 0
        self.aumento = 0
    
    def adicionar(self): 
        misNombres.append(self.nombre)
    
    def dibujar(self):
        if self.vivo:
            image(img[random.randint(0,2)],self.x,self.y)
            
        else:
            image(img[6],self.x,self.y)
    
    def caer(self,velocidad):
        self.y = self.y + velocidad
        
    def saltar(self,velocidad):
        self.y = self.y - velocidad 
        
    def getPuntaje(self):
        return self.puntaje
    
    def setPuntaje(self,puntaje):
        self.puntaje = puntaje
        
    def aumentarPuntaje(self):
        self.puntaje += 1
        self.indicador += 1
        
    def aumentarGravedad(self,aumento):
        self.gravedad = self.gravedad+aumento
        
    def setGravedad(self,gravedad):
        self.gravedad = gravedad

       
class Obstaculo(Elemento):
    velocidad = 10
    
    def __init__(self,x,y):
        Elemento.__init__(self,x,y)
        self.espaciadoH = 200
        self.indicador = True
        self.indicadorAumento = True
        self.aux = self.y - 500 - self.espaciadoH
    
    def dibujar(self):
        image(img[3],self.x,self.y)
        image(img[4],self.x,self.aux)
        
    def mover(self):
        self.x = self.x - self.velocidad
        
    def getIndicador(self):
        return self.indicador
    
    def setIndicador(self,indicador):
        self.indicador = indicador



    