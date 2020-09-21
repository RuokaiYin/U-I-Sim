import torch
from UnarySim.sw.kernel.shiftreg import ShiftReg
from UnarySim.sw.stream.gen import RNG, SourceGen, BSGen
from UnarySim.sw.kernel.add import GainesAdd
from UnarySim.sw.kernel.abs import UnaryAbs
from UnarySim.sw.metric.metric import ProgressiveError

class UnaryEdgeDetect(torch.nn.Module):
    """
    this module is a unary based implementation of Robert's cross operator. Reference to "Using Stochastic Computing to Implement DigitalImage Processing Algorithms."
    """
    def __init__(self,  
                 rng="Sobol",
                 rng_width=1,
                 rng_dim=4,
                 rtype=torch.float,
                 btype=torch.float, 
                 stype=torch.float):
        super(UnaryEdgeDetect, self).__init__()

        self.bitwidth = rng_width
        self.rng_dim = rng_dim
        self.rng = "Sobol"
        self.rtype = rtype
        self.btype = btype
        self.stype = stype

        self.Gx_sub = GainesAdd(mode="bipolar", 
                 scaled=True, 
                 acc_dim=0, 
                 rng=self.rng, 
                 rng_dim=self.rng_dim, 
                 rng_width=1, 
                 rtype=self.rtype, 
                 stype=torch.float)

        self.Gy_sub = GainesAdd(mode="bipolar", 
                 scaled=True, 
                 acc_dim=0, 
                 rng=self.rng, 
                 rng_dim=self.rng_dim+4, 
                 rng_width=1, 
                 rtype=self.rtype, 
                 stype=torch.float)

        self.G_add = GainesAdd(mode="bipolar", 
                scaled=True, 
                acc_dim=0, 
                rng=self.rng, 
                rng_dim=self.rng_dim+8, 
                rng_width=1, 
                rtype=self.rtype, 
                stype=torch.float)

        self.GxAbs = UnaryAbs(depth=8, shiftreg=False, interleave = False, stype=self.stype, btype=self.btype)
        self.GyAbs = UnaryAbs(depth=8, shiftreg=False, interleave = False, stype=self.stype, btype=self.btype)

        self.Gx=0
        self.Gy=0
        self.Gx_abs=0
        self.Gy_abs=0


    
    def forward(self, inp_Pr_i_j, inp_Pr_i1_j1, inp_Pr_i1_j, inp_Pr_i_j1):

        Pr_i_j = inp_Pr_i_j.type(self.stype)
        Pr_i1_j1 = inp_Pr_i1_j1.type(self.stype)
        Pr_i1_j = inp_Pr_i1_j.type(self.stype)
        Pr_i_j1 = inp_Pr_i_j1.type(self.stype)

        Gx_inp = torch.stack([Pr_i_j,1-Pr_i1_j1],0)
        Gy_inp = torch.stack([Pr_i_j1,1-Pr_i1_j],0)

        self.Gx = self.Gx_sub(Gx_inp)
        self.Gy = self.Gy_sub(Gy_inp)

        self.Gx_abs = self.GxAbs(self.Gx)[1]
        self.Gy_abs = self.GyAbs(self.Gy)[1]

        G_inp = torch.stack([self.Gx_abs,self.Gy_abs],0)

        Ps_i_j = self.G_add(G_inp)

        output = Ps_i_j

        return output.type(self.stype)
