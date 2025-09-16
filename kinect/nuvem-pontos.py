import matplotlib
matplotlib.use('TkAgg') # Ou 'Qt5Agg', 'Qt4Agg', 'Agg', etc.

import freenect
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parâmetros intrínsecos aproximados para a câmera de profundidade do Kinect v1
# Estes valores são aproximados e podem variar ligeiramente entre dispositivos.
# Para maior precisão, você pode precisar calibrar seu próprio Kinect.
FX_DEPTH = 594.21  # Distância focal em X (pixels)
FY_DEPTH = 591.04  # Distância focal em Y (pixels)
CX_DEPTH = 339.5   # Ponto principal em X (pixels)
CY_DEPTH = 242.73  # Ponto principal em Y (pixels)

def raw_depth_to_meters(raw_depth_array):
    """
    Converte os valores de profundidade brutos (11-bit) do Kinect v1 para metros.
    Esta é uma fórmula de conversão comum para o Kinect Xbox 360.
    """
    # Evita divisão por zero para valores de profundidade muito baixos
    # onde a fórmula pode resultar em denomidador próximo de zero ou negativo.
    # Adiciona um pequeno epsilon ou filtra esses valores.
    # Aqui, definimos uma máscara para valores válidos e aplicamos a fórmula.
    
    # Os valores raw_depth são de 0 a 2047.
    # A fórmula é baseada em testes e calibração da comunidade OpenKinect.
    
    # Evita um erro de tipo ao converter numpy array em float antes da operação.
    # Garante que as operações matemáticas sejam feitas com floats.
    raw_depth_array_float = raw_depth_array.astype(np.float32)

    # A função original que causa o erro espera uma entrada de profundidade em mm,
    # enquanto o freenect.sync_get_depth() retorna valores brutos (0-2047).
    # A fórmula a seguir é uma conversão comum para o sensor CMOS do Kinect (PMD CamBoard).
    # Ela converte o valor bruto para uma distância que pode ser em mm ou diretamente relacionada.
    
    # Fórmula baseada na documentação não oficial do Kinect ou implementações comuns:
    # depth = 1.0 / (raw_depth * -0.0030711016 + 3.3309495161)
    # A escala para metros precisa ser ajustada dependendo da saída desejada.
    # Se a saída for em milímetros e precisarmos em metros, dividimos por 1000.

    # Vamos usar uma abordagem mais direta se os valores brutos forem mapeados linearmente
    # para uma profundidade máxima, e então converter para metros.
    # No entanto, a relação é não-linear. A fórmula mais precisa para o raw 11-bit Kinect
    # geralmente se parece com esta:
    
    # Para o Kinect v1 (Xbox 360), o raw_depth de 0 a 2047.
    # A profundidade em metros pode ser aproximada por:
    # 1.0 / (raw_depth * k1 + k2)
    # onde k1 e k2 são constantes de calibração.
    # O `freenect` C library tem uma função que mapeia isso.
    # Se ela não está disponível no wrapper Python, podemos usar uma aproximação.

    # Vamos usar a lógica mais robusta que o Freenect usa internamente se não tivermos
    # acesso direto à função.
    # A função Freenect `freenect_get_depth_mm()` faz uma transformação dos 11-bits brutos
    # para milímetros. O `depth_mm_to_meters` do C API espera isso.
    # O Python wrapper pode não ter exposto a conversão intermediária.

    # Vamos usar uma conversão linear simples para teste, ou a inversa de uma função logarítmica,
    # que é o que os sensores CMOS (como o do Kinect) tendem a usar.
    # A forma mais comum de lidar com isso no Python sem a função específica é esta:
    # Os valores de profundidade brutos são 11 bits, de 0 a 2047.
    # Um valor de 2047 geralmente significa que está fora de alcance ou inválido.
    
    # Vamos adaptar uma função de conversão com base em exemplos conhecidos:
    
    # Cria uma cópia para evitar modificar o array original em-place
    depth_array_meters = np.zeros_like(raw_depth_array_float)
    
    # Aplica a máscara para processar apenas valores válidos (não 0 ou 2047/fora de alcance)
    valid_mask = (raw_depth_array_float > 0) & (raw_depth_array_float < 2047)
    
    # A fórmula exata pode variar, mas uma aproximação comum é baseada em:
    # depth_in_mm = 1000.0 / (raw_depth_value * -0.0030711016 + 3.3309495161)
    # E então converter para metros: depth_in_meters = depth_in_mm / 1000.0
    
    # Combinando:
    # depth_in_meters = 1.0 / (raw_depth_value * -0.0030711016 + 3.3309495161)
    
    # Cuidado com o denominador próximo de zero para raw_depth_value pequenos ou grandes.
    # Vamos usar uma implementação mais segura que evita o `AttributeError` e se baseia na matemática.
    # Uma forma robusta, inspirada no próprio `libfreenect` C:
    # depth_in_meters = 0.1236 * np.tan(raw_depth_array_float[valid_mask] / 2842.5 + 1.1863)
    # Ou uma forma mais simples e linearizada para distâncias curtas (menos precisa):
    
    # Vamos tentar a implementação comum para o sensor infravermelho CMOS do Kinect v1.
    # Os valores de profundidade brutos (0-2047) são inversamente proporcionais à distância.
    # raw_depth = IR_max / distance_in_mm + offset
    # distance_in_mm = IR_max / (raw_depth - offset)
    # A `libfreenect` tem uma tabela de lookup ou uma função complexa para isso.
    
    # Dada a ausência da função, a melhor aposta é uma aproximação que se assemelha
    # ao comportamento esperado, ou uma regressão linear para uma faixa de profundidade.
    
    # Uma maneira de simular o comportamento de `depth_mm_to_meters`
    # é usar a tabela de lookup que a libfreenect C usa.
    # No entanto, reproduzir a tabela aqui é inviável para um script de teste.
    
    # A solução mais robusta é instalar uma versão do `python-freenect`
    # que exponha essa funcionalidade ou usar a fórmula inversa.
    
    # Assumindo que raw_depth é um valor 'quantizado' da profundidade,
    # vamos usar uma aproximação inversa para o Kinect v1:
    # Valores de profundidade brutos são convertidos para metros.
    # Os valores de profundidade são 11 bits, de 0 a 2047.
    # 2047 geralmente indica "nenhum dado".
    
    # Fórmula aproximada comum para o Kinect v1 (distância em mm):
    # depth_mm = 1.0 / (raw_value * -0.0030711016 + 3.3309495161)
    # E então converter para metros:
    
    # Vamos aplicar a fórmula apenas aos valores válidos para evitar NaN/inf
    valid_depth_values = raw_depth_array_float[valid_mask]
    
    # Garante que o denominador não seja zero ou muito próximo de zero
    # Adicionamos um pequeno epsilon para robustez se os valores raw forem muito baixos.
    # Valores de `raw_depth_array_float[valid_mask]` são > 0.
    # Se `3.3309495161 - (valid_depth_values * 0.0030711016)` for zero ou negativo, teremos problemas.
    # O Kinect geralmente retorna valores brutos a partir de um certo limite de profundidade.
    
    # Esta é a formula de conversão que a libfreenect tipicamente usa para 11-bit:
    # return 0.1236 * tan(val / 2842.5 + 1.1863);
    # Onde 'val' é o valor raw_depth.
    # Esta função está em `libfreenect/src/depth.c` como `freenect_get_depth_meters`.
    # Aparentemente, o wrapper Python não a expôs como `depth_mm_to_meters` diretamente.
    
    # Vamos implementá-la em numpy para eficiência:
    # A conversão precisa de `np.tan` e os valores precisam ser em radianos.
    
    # Garanta que a função tan seja aplicada aos argumentos corretos e que o tipo de dado seja float.
    depth_array_meters[valid_mask] = 0.1236 * np.tan(valid_depth_values / 2842.5 + 1.1863)

    return depth_array_meters

def get_depth_and_point_cloud():
    """
    Captura um frame de profundidade do Kinect e o converte em uma nuvem de pontos 3D.
    """
    print("Capturando frame de profundidade...")
    # Obtém um frame de profundidade bruto (11-bit) do Kinect
    raw_depth, _ = freenect.sync_get_depth()

    # Converte os valores de profundidade brutos para metros usando a função personalizada
    depth_in_meters = raw_depth_to_meters(raw_depth)

    # Obtém as dimensões da imagem de profundidade
    rows, cols = depth_in_meters.shape

    # Inicializa arrays para as coordenadas X, Y, Z
    # Usaremos arrays 1D para facilitar a plotagem no scatter 3D
    points_x = []
    points_y = []
    points_z = []

    # Itera sobre cada pixel da imagem de profundidade
    for v in range(rows):
        for u in range(cols):
            z = depth_in_meters[v, u] # Profundidade em metros

            # Ignora pontos com profundidade zero ou muito altos (geralmente inválidos)
            # Um limite de 10 metros é razoável para o Kinect v1
            if z > 0 and z < 10:
                # Calcula as coordenadas X e Y no espaço 3D usando o modelo de câmera pinhole
                x = (u - CX_DEPTH) * z / FX_DEPTH
                y = (v - CY_DEPTH) * z / FY_DEPTH

                points_x.append(x)
                points_y.append(y)
                points_z.append(z)

    return np.array(points_x), np.array(points_y), np.array(points_z)

if __name__ == "__main__":
    print("Iniciando a captura da nuvem de pontos do Kinect...")
    print("Certifique-se de que o Kinect esteja conectado e as regras udev configuradas.")
    print("Uma janela 3D será aberta com a nuvem de pontos. Feche-a para sair.")

    try:
        # Captura a nuvem de pontos
        points_x, points_y, points_z = get_depth_and_point_cloud()

        if len(points_x) == 0:
            print("Nenhuma nuvem de pontos válida capturada.")
            print("Isso pode acontecer se o Kinect não estiver vendo nada, estiver muito perto/longe, ou se houver um problema de conexão/permissão.")
        else:
            # Cria a figura 3D
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            # Plota os pontos
            # O 's=1' define o tamanho do ponto, 'c=points_z' colore os pontos pela profundidade
            ax.scatter(points_x, points_y, points_z, s=1, c=points_z, cmap='viridis')

            # Define os rótulos dos eixos
            ax.set_xlabel('X (metros)')
            ax.set_ylabel('Y (metros)')
            ax.set_zlabel('Z (metros)')
            ax.set_title('Nuvem de Pontos do Kinect')

            # Ajusta os limites dos eixos para uma visualização melhor (opcional)
            # Isso tenta centralizar a visualização e dar uma proporção mais "real"
            max_range = np.array([points_x.max()-points_x.min(),
                                  points_y.max()-points_y.min(),
                                  points_z.max()-points_z.min()]).max() / 2.0
            mid_x = (points_x.max()+points_x.min()) * 0.5
            mid_y = (points_y.max()+points_y.min()) * 0.5
            mid_z = (points_z.max()+points_z.min()) * 0.5
            
            # Para evitar erros se o max_range for muito pequeno (e.g., todos os pontos no mesmo lugar)
            if max_range == 0:
                max_range = 0.5 # Valor padrão para evitar problemas de escala

            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)

            # Exibe o gráfico
            plt.show()

    except freenect.FreenectError as e:
        print(f"\nErro ao inicializar ou acessar o Kinect: {e}")
        print("Possíveis causas:")
        print("1. Kinect não conectado ou não ligado.")
        print("2. Regras udev não configuradas ou não recarregadas (veja o guia de instalação anterior).")
        print("3. Outro processo está usando o Kinect.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
    finally:
        print("Teste de nuvem de pontos finalizado.")