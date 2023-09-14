import numpy as np 
import scipy
import sys
import os

def get_size(file):
    """
    Retorna o tamanho em megabytes de um dicionário e seus valores.

    Args:
        file (string): caminho do arquivo.

    Returns:
        float: O tamanho do dicionário e seus valores em megabytes.

    Raises:
        None
    """
    try:
        file_stats = os.stat(file)
        file_size = file_stats.st_size
        print(f"File Size is {file_size / (1024 * 1024):.2f}MB")
    except FileNotFoundError:
        print("File not found.")

def get_numpy(data):
    """
    Converte os dados em formato de dicionário para matrizes NumPy.

    Args:
        data (dict): Dados no formato JSON armazenados em um tipo dicionário contendo informações sobre os valores de tensão de simulação.

    Returns:
        tuple: Uma tupla contendo um array NumPy representando os tempos e uma matriz NumPy representando os valores de tensão.
    """
    mapa = np.zeros((len(data['simData']['V_soma']), len(data['simData']['t'])))
    t = np.array(data['simData']['t'])
    for i, value in enumerate(data['simData']['V_soma'].values()):
        mapa[i] = value
    return t, mapa

def find_peaks(t_arr, v_arr, only_id=False):
    """
    Encontra os picos em um sinal de forma de onda.

    Args:
        t_arr (array-like): Uma matriz de tempos correspondentes aos valores do sinal de forma de onda.
        v_arr (array-like): Uma matriz de valores do sinal de forma de onda.
        only_id (bool, optional): Indica se apenas os IDs dos picos devem ser retornados. O padrão é False.

    Returns:
        tuple or numpy.ndarray: Se only_id for False, retorna uma tupla contendo os IDs dos picos, tempos correspondentes e valores correspondentes. Se only_id for True, retorna apenas os IDs dos picos.
    """
    peaks_id, _ = scipy.signal.find_peaks(v_arr, height=0)
    t = t_arr[peaks_id]
    v = v_arr[peaks_id]
    if only_id:
        peaks_id
    else:
        return peaks_id, t, v


def phase_of_v(t_sample, v_sample, return_peaks=False):
    """
    Calcula as fases de um sinal de forma de onda em relação aos picos.

    Args:
        t_sample (array-like): Uma matriz de tempos correspondentes aos valores do sinal de forma de onda.
        v_sample (array-like): Uma matriz de valores do sinal de forma de onda.

    Returns:
        numpy.ndarray: Uma matriz contendo as fases calculadas para cada neurônio em relação aos picos.

    Raises:
        None
    """
    peaksmat, t_peaks = [], [],  # listas para encontrar id e tempo dos picos
    for v in v_sample:
        peaks_id, t_peak, _ = find_peaks(t_sample, v)
        peaksmat.append(peaks_id)
        t_peaks.append(t_peak)
    id_first_spk = max([min(peak) for peak in peaksmat]) # dos menore spk o maior
    id_last_spk = min([max(peak) for peak in peaksmat]) # id do primeiro dos ultimos spk 

    t_range = t_sample[id_first_spk:id_last_spk]  # tempo onde a phase é definida
    phi = lambda t, t0, t1 : 2*np.pi*(t-t0)/(t1 - t0)  # calcular fase
    phases = np.zeros((len(peaksmat), len(t_range)))  # phases dos n neurônios

    # para cada id do pico n-esimo neuronio
    for n, peak in enumerate(peaksmat):
        # para cada ISI do neurônio
        for t0, t1 in zip(t_sample[peak][:], t_sample[peak][1:]):
            # para cada tempo i onde definimos a fase:
            for i, t in enumerate(t_range):
                if t0 < t <t1:
                    # calcula a fase phi e adiciona no array
                    phases[n,i] = phi(t,t0,t1)
    if return_peaks:
        return t_range, phases, peaksmat, t_peaks, id_first_spk, id_last_spk
    else:    
        return t_range, phases


def kuramoto_param_global_order(spatial_phase_arr):
    """
    Calculates the global order parameter of Kuramoto for a set of spatial phases.

    Args:
        spatial_phase_arr (numpy.ndarray): Array representing the spatial phase distribution of neurons.

    Returns:
        float: Value of the global order parameter of Kuramoto.

    """
    n = len(spatial_phase_arr)
    somatorio = 0
    for j in range(n):
        j = j % n
        somatorio += np.exp(complex(0, spatial_phase_arr[j]))
    z = np.abs(somatorio) / n
    return z

def kuramoto_param_local_order(spatial_phase_arr, delta):
    """
    Calculates the Kuramoto parameter order for a given spatial phase distribution.

    Args:
        spatial_phase_arr (numpy.ndarray): Array representing the spatial phase distribution of neurons.
        delta (int): Window of neighboring neurons to consider.

    Returns:
        numpy.ndarray: Array of Kuramoto parameter order values for each neuron.
    """
    n = len(spatial_phase_arr)
    z = np.zeros_like(spatial_phase_arr)

    for i in range(n):
        somatorio = 0
        for vizinhos in range(i - delta, i + delta + 1):
            j = vizinhos % n
            somatorio += np.exp(complex(0, spatial_phase_arr[j]))
        z[i] = np.abs(somatorio / (int(2*delta)+1))
    return z


def mean_lop_window(lop, window):
    """
    Calcula a média de janelas deslizantes em um conjunto de dados.

    Args:
        lop (numpy.ndarray): Array contendo os dados do parâmetro de ordem local (LOP)
        window (int): O tamanho da janela deslizante.
        ti (float): O valor inicial da janela de tempo.
        tf (float): O valor final da janela de tempo.

    Returns:
        tuple: Uma tupla contendo um array NumPy representando os tempos das janelas e um array NumPy representando a média dos dados em cada janela.

    Raises:
        None
    """
    n_arrays = lop.shape[0] // window
    lop_window = np.array_split(lop, n_arrays)
    mlw = np.zeros((n_arrays,lop.shape[1]))
    for i, arr_window in enumerate(lop_window):
        mlw[i] = np.mean(arr_window, axis=0)
    mlw = np.transpose(mlw)
    return mlw

def time_to_coherence(gop, t, gop_threshold = 0.90, percent_threshold=0.8):
    """
    Calcula o tempo necessário para atingir uma coerência específica.

    Esta função recebe duas listas, 'gop' e 't', representando as métricas de GOP (Global Order Parameter)
    e os tempos correspondentes, respectivamente.

    A função calcula a porcentagem de valores de GOP acima do limite 'gop_threshold'
    até que essa porcentagem alcance o limite 'percent_threshold'. Quando essa condição é
    satisfeita, o tempo correspondente é considerado o tempo de coerência (t_coherence).

    Args:
        gop (list[float]): Uma lista de valores de métricas de GOP.
        t (list[float]): Uma lista de tempos correspondentes às métricas de GOP.
        gop_threshold (float, optional): Limite de métricas de GOP para considerar como "coerentes".
                                         Padrão é 0.85.
        percent_threshold (float, optional): Limite de porcentagem para considerar que a coerência foi atingida.
                                             Padrão é 0.8.

    Returns:
        tuple: Uma tupla contendo o tempo necessário para atingir a coerência desejada e a lista
               de porcentagens de valores de GOP acima do limite em cada etapa de cálculo.

    Raises:
        None

    Example:
        gop = [0.87, 0.92, 0.95, 0.91, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
        t = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ]
        coherence_time = time_to_coherence(gop, t)
        print(coherence_time)  # Saída esperada: 1.0

        gop = [0.87, 0.92, 0.95, 0.91, 0.91, 0.91, 0.91, 0.91, 0.91, 0.91]
        t = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ]
        coherence_time = time_to_coherence(gop, t)
        print(coherence_time)  # Saída esperada: 0.5
    """
    percent, counter, i, t_coherence = 0, 0, 0, 0
    percents = []

    try:
        while percent < percent_threshold:
            if gop[i] > gop_threshold:
                counter += 1
            percent = counter / len(gop[:i+1])
            percents.append(percent)
            if percent >= percent_threshold:
                t_coherence = t[i]
            i += 1
    except (ValueError, IndexError):
        t_coherence = t[i - 1]

    return t_coherence, percents


def t_convergencia_gop(gop, t_sample, std_thresholds, win=10000):
    """
    Calcula o tempo de convergência com base na dispersão do parâmetro GOP (Global Order Parameter).

    Esta função recebe um array 'gop', onde cada elemento representa o valor de GOP,
    e um array 't_sample', que contém os tempos correspondentes às séries temporais de GOP.

    A função calcula o tempo em que a dispersão móvel do GOP atinge um limiar 'std_thresholds' após
    uma janela de 'win' pontos consecutivos. Esse tempo é considerado o tempo de convergência.

    Args:
        gop (numpy.ndarray): Um array de parâmetros GOP.
        t_sample (numpy.ndarray): Um array de tempos correspondentes às séries temporais de GOP.
        win (int, optional): O tamanho da janela deslizante para o cálculo da dispersão. Padrão é 10000.
        std_thresholds (list of float): Uma lista de limiares de dispersão para determinar a convergência.

    Returns:
        tuple (numpy.ndarray, numpy.ndarray): Uma tupla contendo um array NumPy com os tempos de convergência para cada limiar
        e um array NumPy contendo as dispersões calculadas para cada janela.

    Raises:
        None
    """

    std = np.zeros(len(gop) - win)
    t_coherences = np.zeros(len(std_thresholds))
    i = 0

    try:
        gates = np.full(len(std_thresholds), True) # gates of threholds 
        while np.std(gop[i:i+win]) > np.min(std_thresholds):
            std[i] = np.std(gop[i:i+win])
            for g, (n, threshold) in zip(gates , enumerate(std_thresholds)):
                if g and std[i] < threshold:
                    t_coherences[n] = t_sample[i]
                    gates[n] = False 
            i += 1

        for n, g in enumerate(gates):
            if g:
                t_coherences[n] = t_sample[i]
        print('** End While')
        print(f'~> GOP t_coherences:\n \t{t_coherences}')
        return t_coherences, std
    except (ValueError, IndexError):
        print('** IndexError')
        for n, g in enumerate(gates):
            if g:
                t_coherences[n] = t_sample[i-1]
            else:
                t_coherences[n] = t_coherences[n]
        print(f'~> GOP t_coherences:\n \t{t_coherences}')
        return t_coherences, std
    
def t_convergencia_lop(lop, t_sample, std_thresholds, win=10000):
    """
    Calcula o tempo de convergência com base na dispersão do parâmetro LOP (Local Order Parameter).

    Esta função recebe um array 'lop', onde cada elemento representa o valor de LOP de cada elemento,
    e um array 't_sample', que contém os tempos correspondentes às séries temporais de LOP.

    A função calcula o tempo em que a dispersão móvel do LOP espacial médio atinge um limiar 'std_thresholds' após
    uma janela de 'win' pontos consecutivos. Esse tempo é considerado o tempo de convergência.

    Args:
        lop (numpy.ndarray): Um array de parâmetros LOP.
        t_sample (numpy.ndarray): Um array de tempos correspondentes às séries temporais de GOP.
        win (int, optional): O tamanho da janela deslizante para o cálculo da dispersão. Padrão é 10000.
        std_thresholds (list of float): Uma lista de limiares de dispersão para determinar a convergência.

    Returns:
        tuple (numpy.ndarray, numpy.ndarray): Uma tupla contendo um array NumPy com os tempos de convergência para cada limiar
        e um array NumPy contendo as dispersões calculadas para cada janela.

    Raises:
        None
    """

    lop_mean = lop.mean(axis=1)
    std = np.zeros(len(lop_mean) - win)
    t_coherences = np.zeros(len(std_thresholds))
    i = 0

    try:
        gates = np.full(len(std_thresholds), True) # gates of threholds 
        while np.std(lop_mean[i:i+win]) > np.min(std_thresholds):
            std[i] = np.std(lop_mean[i:i+win])
            for g, (n, threshold) in zip(gates , enumerate(std_thresholds)):
                if g and std[i] < threshold:
                    t_coherences[n] = t_sample[i]
                    gates[n] = False 
            i += 1

        for n, g in enumerate(gates):
            if g:
                t_coherences[n] = t_sample[i]
        print('** End While')
        print(f'~> LOP t_coherences:\n \t{t_coherences}')
        return t_coherences, std
    except (ValueError, IndexError):
        print('** IndexError')
        for n, g in enumerate(gates):
            if g:
                t_coherences[n] = t_sample[i-1]
            else:
                t_coherences[n] = t_coherences[n]
        print(f'~> LOP t_coherences:\n \t{t_coherences}')
        return t_coherences, std