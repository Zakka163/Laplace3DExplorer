classdef solver3D
    % Inputs: (Lx, Ly, Lz, dx, BC, method, omega, tol, maxIter)
    
    properties
        Lx, Ly, Lz
        dx
        BC
        method
        omega
        tol
        maxIter
        
        nx, ny, nz
        X, Y, Z
        T
        iter
        err
    end
    
    methods
        function obj = solver3D(Lx, Ly, Lz, dx, BC, method, omega, tol, maxIter)
            if nargin == 0; return; end
            if nargin < 6; method = 'sor'; end
            if nargin < 7; omega = 1.5; end
            if nargin < 8; tol = 1e-6; end
            if nargin < 9; maxIter = 1000; end
            
            obj.Lx = Lx; obj.Ly = Ly; obj.Lz = Lz;
            obj.dx = dx;
            obj.BC = BC;
            obj.method = method;
            obj.omega = omega;
            obj.tol = tol;
            obj.maxIter = maxIter;
            
            obj = obj.initGrid();
            obj = obj.applyBC();
        end
        
        function obj = initGrid(obj)
            x = 0:obj.dx:obj.Lx;
            y = 0:obj.dx:obj.Ly;
            z = 0:obj.dx:obj.Lz;
            
            obj.nx = length(x);
            obj.ny = length(y);
            obj.nz = length(z);
            
            [obj.X, obj.Y, obj.Z] = meshgrid(x, y, z);
            obj.T = zeros(obj.ny, obj.nx, obj.nz);
        end
        
        function obj = applyBC(obj)
            avg_temp = mean([obj.BC.left, obj.BC.right, obj.BC.front, obj.BC.back, obj.BC.bottom, obj.BC.top]);
            obj.T(:) = avg_temp;
            
            obj.T(:, 1, :) = obj.BC.left;
            obj.T(:, obj.nx, :) = obj.BC.right;
            obj.T(1, :, :) = obj.BC.front;
            obj.T(obj.ny, :, :) = obj.BC.back;
            obj.T(:, :, 1) = obj.BC.bottom;
            obj.T(:, :, obj.nz) = obj.BC.top;
        end
        
        function obj = solve(obj)
            obj.iter = 0;
            obj.err = inf;
            
            switch lower(obj.method)
                case 'gauss-elimination'
                    obj = obj.solveGaussElimination();
                case 'liebmann'
                    obj = obj.solveIterative(1.0, false);
                case 'sor'
                    obj = obj.solveIterative(obj.omega, false);
                case 'jacobi'
                    obj = obj.solveIterative(1.0, true);
            end
        end
        
        function obj = solveGaussElimination(obj)
            num_internal = (obj.nx-2) * (obj.ny-2) * (obj.nz-2);
            idx = @(i,j,k) (k-2)*(obj.nx-2)*(obj.ny-2) + (j-2)*(obj.ny-2) + (i-1);
            
            row = zeros(num_internal*7, 1);
            col = zeros(num_internal*7, 1);
            val = zeros(num_internal*7, 1);
            b = zeros(num_internal, 1);
            
            count = 0;
            for k = 2:obj.nz-1
                for j = 2:obj.nx-1
                    for i = 2:obj.ny-1
                        p = idx(i, j, k);
                        
                        count = count + 1;
                        row(count) = p; col(count) = p; val(count) = -6;
                        
                        if j > 2; count=count+1; row(count)=p; col(count)=idx(i,j-1,k); val(count)=1; else; b(p) = b(p) - obj.T(i,j-1,k); end
                        if j < obj.nx-1; count=count+1; row(count)=p; col(count)=idx(i,j+1,k); val(count)=1; else; b(p) = b(p) - obj.T(i,j+1,k); end
                        
                        if i > 2; count=count+1; row(count)=p; col(count)=idx(i-1,j,k); val(count)=1; else; b(p) = b(p) - obj.T(i-1,j,k); end
                        if i < obj.ny-1; count=count+1; row(count)=p; col(count)=idx(i+1,j,k); val(count)=1; else; b(p) = b(p) - obj.T(i+1,j,k); end
                        
                        if k > 2; count=count+1; row(count)=p; col(count)=idx(i,j,k-1); val(count)=1; else; b(p) = b(p) - obj.T(i,j,k-1); end
                        if k < obj.nz-1; count=count+1; row(count)=p; col(count)=idx(i,j,k+1); val(count)=1; else; b(p) = b(p) - obj.T(i,j,k+1); end
                    end
                end
            end
            
            A = sparse(row(1:count), col(1:count), val(1:count), num_internal, num_internal);
            T_int = A \ b;
            
            for k = 2:obj.nz-1
                for j = 2:obj.nx-1
                    for i = 2:obj.ny-1
                        obj.T(i,j,k) = T_int(idx(i,j,k));
                    end
                end
            end
            obj.iter = 1;
            obj.err = 0;
        end
        
        function obj = solveIterative(obj, w, isJacobi)
            while obj.iter < obj.maxIter && obj.err > obj.tol
                T_old = obj.T;
                T_new = obj.T;
                for k = 2:obj.nz-1
                    for j = 2:obj.nx-1
                        for i = 2:obj.ny-1
                            if isJacobi
                                T_new(i, j, k) = (T_old(i+1, j, k) + T_old(i-1, j, k) + ...
                                                  T_old(i, j+1, k) + T_old(i, j-1, k) + ...
                                                  T_old(i, j, k+1) + T_old(i, j, k-1)) / 6.0;
                            else
                                T_GS = (obj.T(i+1, j, k) + obj.T(i-1, j, k) + ...
                                        obj.T(i, j+1, k) + obj.T(i, j-1, k) + ...
                                        obj.T(i, j, k+1) + obj.T(i, j, k-1)) / 6.0;
                                obj.T(i, j, k) = obj.T(i, j, k) + w * (T_GS - obj.T(i, j, k));
                            end
                        end
                    end
                end
                
                if isJacobi
                    obj.T = T_new;
                end
                
                obj.err = max(abs(obj.T(:) - T_old(:)));
                obj.iter = obj.iter + 1;
            end
        end
    end
end
