from matplotlib import pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
np.random.seed(5718925)

def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plot_params()
def GOP(spatial_phase_arr):
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

def LOP(spatial_phase_arr, delta):
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
n = 100

dente_serra = lambda x, periodo: (x % (periodo)) / 4.4*np.pi

phase_rand = 2 * np.pi * np.random.random_sample(n)
# phase_sin = np.linspace(0, 2*np.pi, n)
phase_sin = np.array([dente_serra(x,5) for x in range(100)])
phase_chimera = np.array([phi if i < 0.2*(len(phase_rand)) or i > 0.7*(len(phase_rand)) else 5e-2*phi for i, phi in enumerate(phase_rand)])
phase_coerente = np.array([0.5 for i in range(n)])

lops_rand_mean = np.zeros((len(phase_rand)))
lops_sin_mean = np.zeros((len(phase_rand)))
lops_chimera_mean = np.zeros((len(phase_rand)))
lops_coerente_mean = np.zeros((len(phase_rand)))

for delta in range(len(phase_rand)):
    lops_rand_mean[delta] = LOP(phase_rand, delta).mean()
    lops_sin_mean[delta] = LOP(phase_sin, delta).mean()
    lops_chimera_mean[delta] = LOP(phase_chimera, delta).mean()
    lops_coerente_mean[delta] = LOP(phase_coerente, delta).mean()

fig = plt.figure(tight_layout=True, figsize=(10,6))
gs = gridspec.GridSpec(4, 4)

ax00 = fig.add_subplot(gs[0,0])
ax00.plot(lops_rand_mean, label='$\overline{LOP}$')
ax00.hlines(y = GOP(phase_rand), xmin=0, xmax=int(len(phase_rand)/2), color='red',linestyle='--', label='GOP')
ax00.vlines(x = 5, ymin=0, ymax=1., color='gray',linestyle='--', label='$\delta=5$')
ax00.set_title('Métricas', pad=20)
ax00.set_ylim(0,1)
ax00.set_xlim(0,int(len(phase_rand)/2))
ax00.set_ylabel('GOP e $\overline{LOP}$')
ax00.set_xlabel(r'$\delta$')
ax00.spines['top'].set_visible(False)
ax00.spines['right'].set_visible(False)
plt.legend()

ax10 = fig.add_subplot(gs[1,0])
ax10.plot(lops_sin_mean, label='LOP')
ax10.hlines(y = GOP(phase_sin), xmin=0, xmax=int(len(phase_sin)/2), color='red',linestyle='--', label='GOP')
ax10.vlines(x = 5, ymin=0, ymax=1., color='gray',linestyle='--', label='$\delta=5$')
ax10.set_ylim(0,1)
ax10.set_xlim(0,int(len(phase_sin)/2))

ax10.set_ylabel('GOP e $\overline{LOP}$')
ax10.set_xlabel(r'$\delta$')
ax10.spines['top'].set_visible(False)
ax10.spines['right'].set_visible(False)

ax20 = fig.add_subplot(gs[2,0])
ax20.plot(lops_chimera_mean, label='LOP')
ax20.hlines(y = GOP(phase_chimera), xmin=0, xmax=int(len(phase_chimera)/2), color='red',linestyle='--', label='GOP')
ax20.vlines(x = 5, ymin=0, ymax=1., color='gray',linestyle='--', label='$\delta=5$')
ax20.set_ylim(0,1)
ax20.set_xlim(0,int(len(phase_chimera)/2))
ax20.set_ylabel('GOP e $\overline{LOP}$')
ax20.set_xlabel(r'$\delta$')
ax20.spines['top'].set_visible(False)
ax20.spines['right'].set_visible(False)

ax30 = fig.add_subplot(gs[3,0])
ax30.plot(lops_coerente_mean, label='LOP')
ax30.hlines(y = GOP(phase_coerente), xmin=0, xmax=int(len(phase_chimera)/2), color='red',linestyle='--', label='GOP')
ax30.vlines(x = 5, ymin=0, ymax=1., color='gray',linestyle='--', label='$\delta=5$')
ax30.set_ylim(0,1)
ax30.set_xlim(0,int(len(phase_coerente)/2))
ax30.set_ylabel('GOP e $\overline{LOP}$')
ax30.set_xlabel(r'$\delta$')
ax30.spines['top'].set_visible(False)
ax30.spines['right'].set_visible(False)

ax01 = fig.add_subplot(gs[0,1])
ax11 = fig.add_subplot(gs[1,1])
ax21 = fig.add_subplot(gs[2,1])
ax31 = fig.add_subplot(gs[3,1])

ax01.plot(phase_rand, 'ob',markersize=2)
ax11.plot(phase_sin, 'or',markersize=2)
ax21.plot(phase_chimera, 'og',markersize=2)
ax31.plot(phase_coerente, 'om',markersize=2)

ax01.set_yticks([0, np.pi, 2*np.pi])
ax01.set_yticklabels(['0', '$\pi$', '$2 \pi$']) 
ax01.set_title('Fase Neurônios', pad=20)
ax01.set_ylabel('$\phi$', rotation=0)
ax01.set_xlabel('$n$')

ax11.set_yticks([0, np.pi/2, np.pi])
ax11.set_yticklabels(['0', '$\pi$', '$2 \pi$']) 
ax11.set_ylabel('$\phi$', rotation=0)
ax11.set_xlabel('$n$')

ax21.set_yticks([0, np.pi, 2*np.pi])
ax21.set_yticklabels(['0', '$\pi$', '$2 \pi$']) 
ax21.set_ylabel('$\phi$', rotation=0)
ax21.set_xlabel('$n$')

ax31.set_yticks([0, np.pi, 2*np.pi])
ax31.set_yticklabels(['0', '$\pi$', '$2 \pi$']) 
ax31.set_ylabel('$\phi$', rotation=0)
ax31.set_xlabel('$n$')

plt.savefig('../figures/Convergencia_LOP_to_GOP.png', dpi=600, bbox_inches='tight')

