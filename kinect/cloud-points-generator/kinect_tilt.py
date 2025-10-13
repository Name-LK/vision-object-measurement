import freenect
import sys
import time

def set_tilt_angle(angle_degrees):
    """
    Define o ângulo de inclinação do motor do Kinect.

    Args:
        angle_degrees (int): O ângulo em graus, entre -27 e 27.
    """
    # O ângulo do motor do Kinect V1 tem um limite prático.
    # O intervalo seguro é geralmente entre -27 e 27 graus.
    if not -27 <= angle_degrees <= 27:
        print(f"Erro: O ângulo deve estar entre -27 e 27 graus. Você forneceu {angle_degrees}.")
        return

    print("Inicializando o contexto do freenect...")
    ctx = freenect.init()

    # Tenta abrir o primeiro dispositivo Kinect encontrado (índice 0)
    dev = freenect.open_device(ctx, 0)

    if not dev:
        print("Erro: Não foi possível encontrar ou abrir o dispositivo Kinect.")
        freenect.shutdown(ctx)
        return

    print(f"Dispositivo Kinect encontrado. Movendo para o ângulo: {angle_degrees} graus.")
    
    try:
        # Define o ângulo de inclinação do motor
        freenect.set_tilt_degs(dev, angle_degrees)
        print("Ângulo definido com sucesso.")
        
        # Dê um pequeno tempo para o motor se mover fisicamente
        time.sleep(1)

    finally:
        # Garante que o dispositivo e o contexto sejam fechados
        print("Fechando o dispositivo e o contexto.")
        freenect.close_device(dev)
        freenect.shutdown(ctx)

if __name__ == "__main__":
    # Verifica se um argumento de linha de comando foi fornecido
    if len(sys.argv) != 2:
        print("Uso: python mover_kinect.py <angulo>")
        print("Exemplo: python mover_kinect.py 15")
        sys.exit(1)

    try:
        # Converte o argumento para um número inteiro
        angle = int(sys.argv[1])
        set_tilt_angle(angle)
    except ValueError:
        print("Erro: O ângulo fornecido não é um número válido.")
        sys.exit(1)