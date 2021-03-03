import cv2 
import numpy as np

# Criterios de interrupção do otimizador
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  

# Cria pontos
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays para armazenar os pontos 3d e 2d de todas as imagens
objpoints = [] # pontos 3d no espaço do mundo real
imgpoints = [] # pontos 2d no plano da imagem


# Captura o video
vid = cv2.VideoCapture(0) 

while(True): 
      
    # Captura cada frame do video
    ret, frame = vid.read() 

    # transforma em cinza para facilitar a busca pelo  padrão
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # usa o opencv para recuperar as bordas do xadrez
    ret, corners = cv2.findChessboardCorners(gray, (7,6), None)

    # Caso ele encontre:
    # 1. cria os 'desenhos' para mostrar as bordas encontradas
    # 2. Insere esses desenhos no frame atual
    # 3. adiciona os pontos mapeados aos arrays
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(frame, (7,6), corners2, True)
        
        objpoints.append(objp)
        imgpoints.append(corners)

    # Mostra o frame atual, pode ou não estar com as bordas coloridas
    cv2.imshow('frame', frame) 

    # Botão q para iniciar a calibração e depois sair do programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("Calibrando...", end='\n\n')

# Realiza a calibração de câmera pelo OpenCV
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Cria uma matriz zerada para incluir os dados dos vetores de rotação
rotation_mat = np.zeros(shape=(3, 3))

# Preenche a matriz com os vetores de rotação devolvidos pelo OpenCV
R = cv2.Rodrigues(rvecs[0], rotation_mat)[0]

# Computa a matriz P, multiplicando a matriz de intrínsecos K pela 
# matriz de rotação, e o vetor de translação
P = np.column_stack( ( np.matmul(mtx,R), tvecs[0] ) )

print("Matriz de projeção P:")
print(P, end='\n\n')

print("matriz de intrínsecos (K):")
print(mtx, end='\n\n')

# print("Vetores de Rotação:")
# print(rvecs[:2])
print("Matriz de rotação:")
print(R, end='\n\n')

print("Vetor de translação:")
#print(np.array(tvecs).flatten(), end='\n\n')
print(tvecs[0], end='\n\n')

print("Parâmetros de distorção: [k1, k2, p1, p2, k3]")
print(dist, end='\n\n')

print(f"RMSE de projeção: {ret}")

# Solta o objeto de captura
vid.release() 

# Destroi as janelas
cv2.destroyAllWindows() 