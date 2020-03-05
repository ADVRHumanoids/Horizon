from horizon import *

class linearized_friction_cone(constraint_class):
    def __init__(self, Force, mu, Rot):
        self.F = Force
        self.mu = mu
        self.R = Rot

    def virtual_method(self, k):

        mu_lin = self.mu / 2.0 * sqrt(2.0)

        A_fr = np.zeros([5, 3])
        A_fr[0, 0] = 1.0
        A_fr[0, 2] = -mu_lin
        A_fr[1, 0] = -1.0
        A_fr[1, 2] = -mu_lin
        A_fr[2, 1] = 1.0
        A_fr[2, 2] = -mu_lin
        A_fr[3, 1] = -1.0
        A_fr[3, 2] = -mu_lin
        A_fr[4, 2] = -1.0

        A_fr_R = mtimes(A_fr, self.R)

        self.gk = [mtimes(A_fr_R, self.F[k])]
        self.g_mink = np.array([-1000., -1000., -1000., -1000., -1000.]).tolist()
        self.g_maxk = np.array([0., 0., 0., 0., 0.]).tolist()

class remove_contact(constraint_class):
    def __init__(self, Force):
        self.F = Force

    def virtual_method(self, k):
        self.gk = [self.F[k]]
        self.g_mink = np.array([0., 0., 0.]).tolist()
        self.g_maxk = np.array([0., 0., 0.]).tolist()