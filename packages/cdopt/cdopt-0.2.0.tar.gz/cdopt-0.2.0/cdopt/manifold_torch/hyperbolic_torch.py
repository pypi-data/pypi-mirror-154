import numpy as np
import torch
from .basic_manifold_torch import basic_manifold_torch

class hyperbolic_torch(basic_manifold_torch):
    def __init__(self, var_shape, B = None, device = torch.device('cpu'), dtype = torch.float64) -> None:
        n = var_shape[0]
        p = var_shape[1]
        self._n = n
        self._p = p
        self.dim = n*p 
        self.device = device
        self.dtype = dtype

        self.var_shape = (n,p)

        self._half_n = int(n/2)
        
        if B is None:
            # idx =  list(range(int(n/2),n)) + list(range(int(n/2) )) 
            # def B(X):
            #     return X[idx,:]



            # In = np.eye(int(n/2))
            # Zero_n = np.zeros((int(n/2),int(n/2)))

            # Jn = np.block([[Zero_n,  In], [In, Zero_n]    ])




            # Jn = torch.tensor(Jn, dtype= self.dtype).to_sparse()
            # Jn = Jn.to(device = self.device, dtype = self.dtype)


            def B(X):
                return torch.cat( (X[self._half_n:, :], X[:self._half_n,:]), 0 )
                # return torch.matmul(Jn, X)



        self.B = B 
        
        super().__init__('Hyperbolic',(n,p), (p,p),   device= self.device ,dtype= self.dtype)
        self._parameters['In'] = torch.eye(self._p).to(device = self.device, dtype = self.dtype)
        self.Ip = self._parameters['In']
        # Here we require B be a function
        #  when one wishes to input a matrix B_mat
        #  we recommand to use lambda X: B@X instead

        

    def Phi(self, M):
        return (M + M.T)/2


    def A(self, X):
        XX = X.T @ self.B(X)
        return 1.5 * X - X @ (XX /2)


    def JA(self, X, D):
        BX = self.B(X)
        return D @ ( 1.5 * self.Ip - 0.5 * X.T @ BX  )  - BX @ self.Phi(X.T @ D)


    def JA_transpose(self, X, D):
        BX = self.B(X)
        return D @ ( 1.5 * self.Ip - 0.5 * X.T @ BX  ) - X @ self.Phi( D.T @ BX )


    def hessA(self, X, gradf, D):
        BX = self.B(X)

        return - self.B(D) @ self.Phi( X.T @ gradf  ) - BX @ self.Phi(D.T @ gradf) - gradf @ self.Phi( D.T @ BX )



    
    def C(self, X):
        return X.T @ self.B(X) - self.Ip

    def C_quad_penalty(self, X):
        return torch.sum(self.C(X) ** 2)



    def JC(self, X, Lambda):
        return 2 * self.B(X) @ self.Phi( Lambda  )


    def hess_feas(self, X, D):
        BX = self.B(X)
        return 4*BX @ self.Phi( BX.T @ D ) + 2*self.B(D) @ (X.T @ BX- self.Ip)



    def Feas_eval(self, X):
        return torch.linalg.norm( self.C(X) , 'fro')

    def Init_point(self, Xinit = None):
        X = Xinit
        if X is None:
            X = torch.randn(self._n, self._p).to(device = self.device, dtype = self.dtype)
            X, R = torch.linalg.qr(X)
        else:
            X = X.detach()

            
        X = X.to(device = self.device, dtype = self.dtype)
        X.requires_grad = True 

        for jl in range(30):
            XX = X.T @ self.B(X)
            feas = torch.linalg.norm( self.C(X) , 'fro')
            # print(feas)
            if feas < 1e-1:
                X = self.A(X)
            else:
                X = X - 0.2* (self.B(X) @ self.C(X))
                # X = np.linalg.solve(0.5 * XX + 0.5 * self.Ip, X.T ).T
                # X = X + 0.00001/self._n * np.random.randn(self._n, self._p)
            if feas < 1e-8:
                break
        return X

    def Post_process(self,X):
        L_process = torch.linalg.cholesky(X.T @ self.B(X))
        X = torch.linalg.solve(L_process, X.T).T
        return X





    def generate_cdf_fun(self, obj_fun, beta):
        return lambda X: obj_fun(self.A(X)) + (beta/2) * self.C_quad_penalty(X)
        




    def generate_cdf_grad(self, obj_grad, beta):
        def local_grad(X):
            BX= self.B(X)
            CX = X.T @ BX - self.Ip
            AX = X - 0.5 * X@CX
            gradf = obj_grad(AX)
            XG = self.Phi(X.T @ gradf)

            # local_JA_gradf = gradf @ (self.Ip - 0.5 * CX) - X @ XG 
            
            # local_JC_CX = 2 * X @(CX)

            return gradf @ (self.Ip - 0.5 * CX) +  BX @  ( 2* beta * CX - XG) 

        return local_grad



    def generate_cdf_hess(self, obj_grad, obj_hess, beta):
        def local_hess(X, D):
            BX= self.B(X)
            CX = X.T @ BX - self.Ip
            AX = X - 0.5 * X@CX
            gradf = obj_grad(AX)
            # XG = self.Phi(X.T @ gradf)



            local_JAT_D =  D @ ( self.Ip - 0.5 * CX  ) - X @ self.Phi( D.T @ BX )
            local_objhess_JAT_D = obj_hess(AX, local_JAT_D)
            # local_JA_objhess_JAT_D = local_objhess_JAT_D @ ( self.Ip - 0.5 * CX  )  - BX @ self.Phi(X.T @ local_objhess_JAT_D)

            # local_hessA_objgrad_D = - self.B(D) @ self.Phi( X.T @ gradf  ) - BX @ self.Phi(D.T @ gradf) - gradf @ self.Phi( D.T @ BX )

            # local_hess_feas = 4*BX @ self.Phi( BX.T @ D ) + 2*self.B(D) @ CX



            return local_objhess_JAT_D @ ( self.Ip - 0.5 * CX  )  - BX @ (self.Phi(X.T @ local_objhess_JAT_D) + self.Phi(D.T @ gradf)  - 4* beta * self.Phi( BX.T @ D )   ) - self.B(D) @ self.Phi( X.T @ gradf -2*beta * CX ) - gradf @ self.Phi( D.T @ BX )


            # return local_JA_objhess_JAT_D + local_hessA_objgrad_D + beta * local_hess_feas

        return local_hess



    def generate_cdf_hess_approx(self, obj_grad, obj_hess, beta):
        def local_hess(X, D):
            BX= self.B(X)
            CX = X.T @ BX - self.Ip
            gradf = obj_grad(X)
            # XG = self.Phi(X.T @ gradf)



            local_JAT_D =  D  - X @ self.Phi( D.T @ BX )
            local_objhess_JAT_D = obj_hess(X, local_JAT_D)
            # local_JA_objhess_JAT_D = local_objhess_JAT_D @ ( self.Ip - 0.5 * CX  )  - BX @ self.Phi(X.T @ local_objhess_JAT_D)

            # local_hessA_objgrad_D = - self.B(D) @ self.Phi( X.T @ gradf  ) - BX @ self.Phi(D.T @ gradf) - gradf @ self.Phi( D.T @ BX )

            # local_hess_feas = 4*BX @ self.Phi( BX.T @ D ) + 2*self.B(D) @ CX



            return local_objhess_JAT_D  - BX @ (self.Phi(X.T @ local_objhess_JAT_D) + self.Phi(D.T @ gradf)  - 4* beta * self.Phi( BX.T @ D )   ) - self.B(D) @ self.Phi( X.T @ gradf -2*beta * CX ) - gradf @ self.Phi( D.T @ BX )

        return local_hess
