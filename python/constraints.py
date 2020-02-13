from horizon import *
import casadi_kin_dyn.pycasadi_kin_dyn as cas_kin_dyn
from inverse_dynamics import *

class contact(constraint_class):
    def __init__(self, FKlink, Q, qinit):
        self.FKlink = FKlink
        self.Q = Q
        self.qinit = qinit

    def virtual_method(self, k):
        CLink_pos_init = self.FKlink(q=self.qinit)['ee_pos']
        CLink_pos = self.FKlink(q=self.Q[k])['ee_pos']
        self.gk = [CLink_pos - CLink_pos_init]
        self.g_mink = np.array([0., 0., 0.]).tolist()
        self.g_maxk = np.array([0., 0., 0.]).tolist()

class torque_lims(constraint_class):
    def __init__(self, id, tau_min, tau_max):
        self.id = id
        self.tau_min = tau_min
        self.tau_max = tau_max

    def virtual_method(self, k):
        self.gk = [self.id.compute(k)]
        self.g_mink = self.tau_min
        self.g_maxk = self.tau_max


class multiple_shooting(constraint_class):
    def __init__(self, X, Qddot, F_integrator):
        self.X = X
        self.Qddot = Qddot
        self.F_integrator = F_integrator

    def virtual_method(self, k):
        integrator_out = self.F_integrator(x0=self.X[k], p=self.Qddot[k])
        self.gk = [integrator_out['xf'] - self.X[k + 1]]
        self.g_mink = [0] * self.X[k + 1].size1()
        self.g_maxk = [0] * self.X[k + 1].size1()

class initial_condition(constraint_class):
    def __init__(self, X0, x_init):
        self.X0 = X0
        self.x_init = x_init

    def virtual_method(self, k):
        self.gk = [self.X0]
        self.g_mink = self.x_init
        self.g_maxk = self.x_init




