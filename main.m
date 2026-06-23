clc; clear; close all;

addpath('solver');
addpath('visualization');

Lx = 1.0; Ly = 1.0; Lz = 1.0;
dx = 0.05;

BC.left = 100; BC.right = 50; 
BC.front = 0; BC.back = 100;
BC.bottom = 95; BC.top = 25; 

omega = 1.8;
tol = 1e-6;
maxIter = 5000;

fprintf('==================================================\n');
fprintf('  Testing Performa Solver Laplace 3D\n');
fprintf('==================================================\n\n');

current_method = 'sor';
fprintf('Menguji Metode: %s...\n', upper(current_method));

tic;
solver = solver3D(Lx, Ly, Lz, dx, BC, current_method, omega, tol, maxIter);
solver = solver.solve(); 
time_elapsed = toc;

mid_y = round(size(solver.T, 1) / 2);
mid_x = round(size(solver.T, 2) / 2);
mid_z = round(size(solver.T, 3) / 2);
T_center = solver.T(mid_y, mid_x, mid_z);

fprintf('  -> Waktu Eksekusi : %.4f detik\n', time_elapsed);
fprintf('  -> Total Iterasi  : %d\n', solver.iter);
fprintf('  -> Error Terakhir : %e\n', solver.err);
fprintf('  -> Suhu di Pusat  : %.2f\n\n', T_center);

fprintf('==================================================\n');
fprintf('  Testing Selesai!\n');
fprintf('==================================================\n');

T = solver.T; X = solver.X; Y = solver.Y; Z = solver.Z;

X2D = X(:, :, mid_z);
Y2D = Y(:, :, mid_z);
T2D = T(:, :, mid_z);

showHeatmap(X2D, Y2D, T2D);
showContour(X2D, Y2D, T2D);
showSurface(X2D, Y2D, T2D);

sliceViewer(X, Y, Z, T);
orthogonalViewer(X, Y, Z, T);

showScatter3D(X, Y, Z, T);
showSlice3D(X, Y, Z, T);
showIsosurface(X, Y, Z, T);
