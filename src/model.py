import numpy as np
from scipy.integrate import solve_ivp

class HodgkinHuxleyModel:
    """
    Simulates the Hodgkin-Huxley squid giant axon model (1952).
    """
    def __init__(
        self,
        g_Na=120.0,  # Max Sodium conductance (mS/cm^2)
        g_K=36.0,    # Max Potassium conductance (mS/cm^2)
        g_L=0.3,     # Leak conductance (mS/cm^2)
        E_Na=50.0,   # Sodium reversal potential (mV)
        E_K=-77.0,   # Potassium reversal potential (mV)
        E_L=-54.387, # Leak reversal potential (mV)
        C_m=1.0      # Membrane capacitance (uF/cm^2)
    ):
        self.g_Na = g_Na
        self.g_K = g_K
        self.g_L = g_L
        self.E_Na = E_Na
        self.E_K = E_K
        self.E_L = E_L
        self.C_m = C_m

    # Voltage-dependent rate constants
    @staticmethod
    def alpha_m(V): return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0)) if abs(V + 40.0) > 1e-7 else 1.0
    
    @staticmethod
    def beta_m(V):  return 4.0 * np.exp(-(V + 65.0) / 18.0)
    
    @staticmethod
    def alpha_h(V): return 0.07 * np.exp(-(V + 65.0) / 20.0)
    
    @staticmethod
    def beta_h(V):  return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))
    
    @staticmethod
    def alpha_n(V): return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0)) if abs(V + 55.0) > 1e-7 else 0.1
    
    @staticmethod
    def beta_n(V):  return 0.125 * np.exp(-(V + 65.0) / 80.0)

    def _derivatives(self, t, state, i_ext_func):
        V, m, h, n = state
        I_ext = i_ext_func(t)

        # Ionic currents
        I_Na = self.g_Na * (m**3) * h * (V - self.E_Na)
        I_K  = self.g_K * (n**4) * (V - self.E_K)
        I_L  = self.g_L * (V - self.E_L)

        # Membrane potential derivative
        dVdt = (I_ext - I_Na - I_K - I_L) / self.C_m

        # Gating variable derivatives
        dmdt = self.alpha_m(V) * (1.0 - m) - self.beta_m(V) * m
        dhdt = self.alpha_h(V) * (1.0 - h) - self.beta_h(V) * h
        dndt = self.alpha_n(V) * (1.0 - n) - self.beta_n(V) * n

        return [dVdt, dmdt, dhdt, dndt]

    def simulate(self, t_max=50.0, dt=0.02, I_inj=10.0, t_start=10.0, t_stop=40.0):
        """
        Runs numerical integration using Runge-Kutta 45 (RK45).
        """
        t_eval = np.arange(0, t_max, dt)

        # Step pulse current function
        i_ext_func = lambda t: I_inj if (t_start <= t <= t_stop) else 0.0

        # Resting state initial values (~ -65 mV)
        V0 = -65.0
        m0 = self.alpha_m(V0) / (self.alpha_m(V0) + self.beta_m(V0))
        h0 = self.alpha_h(V0) / (self.alpha_h(V0) + self.beta_h(V0))
        n0 = self.alpha_n(V0) / (self.alpha_n(V0) + self.beta_n(V0))

        sol = solve_ivp(
            fun=self._derivatives,
            t_span=(0, t_max),
            y0=[V0, m0, h0, n0],
            t_eval=t_eval,
            args=(i_ext_func,),
            method='RK45'
        )

        V, m, h, n = sol.y
        I_inj_arr = np.array([i_ext_func(t) for t in sol.t])
        
        # Calculate resulting currents for plotting
        I_Na = self.g_Na * (m**3) * h * (V - self.E_Na)
        I_K  = self.g_K * (n**4) * (V - self.E_K)
        I_L  = self.g_L * (V - self.E_L)

        return {
            "t": sol.t,
            "V": V,
            "m": m,
            "h": h,
            "n": n,
            "I_inj": I_inj_arr,
            "I_Na": I_Na,
            "I_K": I_K,
            "I_L": I_L
        }