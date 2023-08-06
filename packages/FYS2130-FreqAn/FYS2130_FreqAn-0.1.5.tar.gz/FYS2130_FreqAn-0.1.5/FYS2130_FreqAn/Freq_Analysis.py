import numpy as np
import matplotlib.pyplot as plt
import time

class Freq_Analysis:
    def __init__(self, signal, fs):
        self.signal = signal
        self.fs = fs    # Sample frekvens
        self.dt = 1 / fs    # Tid mellom samplingspunkter
        self.N = len(signal)      # Antall samplingspunkter
        self.T = self.dt*self.N      # Total samplingstid
        self.t = np.linspace(0, self.T, self.N)

    def plot_Fourier(self, xlim=None, show=True):
        self.show_FT = show
        if xlim is None: xlim = self.fs/2
        self.xlim = xlim
        X_k = np.fft.fft(self.signal)   # FT av samplet frekvens
        FT_freq = np.fft.fftfreq(int(self.N), self.dt)     # FT-frekvens (korrekt)
        t = np.linspace(0, self.N*self.dt, int(self.N))

        fig = plt.figure(figsize=(8, 4))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        ax1.plot(t, self.signal, label='Sampled signal')
        ax2.plot(FT_freq, abs(X_k), label='Fourier Transform')
        fig.suptitle('Fourier Transform', weight='bold', fontsize=20)
        ax1.set_xlabel('t [s]', weight='bold', fontsize=18)
        ax1.set_ylabel('x_n', weight='bold', fontsize=18)
        ax2.set_xlabel('f [Hz]', weight='bold', fontsize=18)
        ax2.set_ylabel('X_k', weight='bold', fontsize=18)
        ax2.set_xlim(-xlim, xlim)    # Setter grenser på begge plott så det blir enklere å se, siden de har ulike nyquistfrekvenser

        fig.tight_layout()
        ax1.legend(prop={'size':14}); ax2.legend(prop={'size':14})
        if show is True: plt.show()
        return FT_freq, X_k

    # Morlet-Wavelet
    def wavelet(self, tn, omega_a, tk, K):
        C = 0.798 * omega_a / (fs*K)
        # C = 1
        w = C*(np.exp(-1j*omega_a*(tn - tk)) - np.exp(-K**2))*np.exp(-omega_a**2 * (tn - tk)**2 / (2*K)**2)
        """
        Animerer for å sjekke om wavelet faktisk beveger seg gjennom signal
        (C=1 hensiktsmessig her)
        """
        # plt.plot(tn, x_n, 'k')
        # plt.plot(tn, np.real(w))
        # plt.plot(tn, np.imag(w))
        # plt.draw()
        # plt.ylim(-A2, A2)
        # plt.pause(0.01)
        # plt.clf()
        return w

    # Wavelet-transformasjon i tidsdomenet
    def wavelet_transform(self, x_n, omega_a, tk, K):
        tn = self.t.copy()
        gamma = np.sum(x_n * self.wavelet(tn, omega_a, tk, K).conjugate())
        return gamma

    # Lager selve diagrammet ved å iterere gjennom verdier
    def wavelet_diagram(self, omega_a, K):
        """
        Denne skjer i tidsdomenet, og er vesentlig tregere enn i frekvensdomenet.
        Denne har derfor ikke blitt oppdatert.
        """
        x_n = self.signal.copy()
        self.tk = self.t.copy()
        self.omega_a = omega_a
        N = len(self.tk)
        M = len(omega_a)
        WT = np.zeros([N, M], dtype=np.complex128)
        for m in range(M):
            for n in range(N):
                WT[n,m] = self.wavelet_transform(x_n, self.omega_a[m], self.tk[n], K)

        return WT

    # Fouriertransform av Morlet-wavelet
    def FT_wavelet(self, omega, omega_a, K):
        w = 2 * (np.exp(-(K * (omega - omega_a)/omega_a)**2) - np.exp(-K**2) * np.exp(-(K*omega/omega_a)**2))
        return w


    # Den raskere algoritmen som bruker Konvolusjonsteoremet i frekvensdomenet
    def faster_wavelet_diagram(self, omega_a, K, sample_skip=1, time_start=0, time_end=None, show=True, ani=False):
        if time_end is None: time_end = self.T
        tk = np.linspace(0, self.N*self.dt, int(self.N))[::sample_skip]
        where_to_solve = np.logical_and(tk >= time_start, tk <= time_end)
        tk = tk[where_to_solve]
        N = len(tk)
        fs = 1 / (self.dt*sample_skip)
        dt = 1 / fs
        omega_a_mesh, tk_mesh = np.meshgrid(omega_a, tk, indexing='ij')
        omega_0 = np.fft.fftfreq(int(N), dt) * 2*np.pi
        x_n = self.signal.copy()[::sample_skip]
        x_n = x_n[where_to_solve]
        x_nFT = np.fft.fft(x_n)
        N = len(tk)
        M = len(omega_a)
        WT = np.zeros([M, N], dtype=np.complex128)
        if ani is True:
            x_nFTmax = np.max(abs(x_nFT))
            # Animerer hva som skjerm i en WT i frekvensdomenet
            for j in range(M):
                W = self.FT_wavelet(omega_0, omega_a[j], K)
                Wmax = np.max(W)
                plt.plot(omega_0, abs(x_nFT) / x_nFTmax, 'k', label='FT')
                plt.plot(omega_0, W / Wmax, label='FT-wavelet')     # Normaliserer plottene for illustrasjon
                plt.plot(omega_0, W / Wmax * abs(x_nFT) / x_nFTmax, 'r', label='product')
                plt.draw()
                plt.title("Takes product of the two FT's", weight='bold', fontsize=20)
                plt.xlabel('omega [1/s]', weight='bold', fontsize=20)
                plt.ylabel('FT', weight='bold', fontsize=20)
                plt.xlim(-np.max(omega_a), np.max(omega_a))
                plt.legend()
                plt.pause(0.01)
                plt.clf()
            plt.close()
            # Try-blocken sjekker om self.show_FT eksisterer. Hvis den ikke gjør det så går den videre,
            # hvis den eksisterer sjekker vi om den er false.
            try:
                self.show_FT
            except AttributeError:
                pass
            else:
                if self.show_FT is False: self.plot_Fourier(xlim=self.xlim, show=False)

        # Regner ut selve WT transformasjonen og lagrer verdier
        for i in range(M):
                WT[i, :] = np.fft.ifft(x_nFT * self.FT_wavelet(omega_0, omega_a[i], K)) # Konvolusjonsteoremet

        freq_mesh = omega_a_mesh.copy() / (2*np.pi)
        fig = plt.figure()
        ax = fig.add_subplot()
        p = ax.contourf(tk_mesh, freq_mesh, abs(WT), levels=300, cmap='hot')
        cbar_ax = fig.colorbar(p, ax=ax, aspect=10)

        cbar_ax.set_label('Amplitude', weight='bold', fontsize=20)
        ax.set_xlabel('t [s]', weight='bold', fontsize=20); ax.set_ylabel('freq [1/s]', weight='bold', fontsize=20)
        ax.set_title(f'K = {K}', weight='bold', fontsize=20)

        fig.tight_layout()
        if show is True: plt.show()
        return freq_mesh, tk_mesh, WT
