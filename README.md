# Laplace 3D Explorer

![MATLAB](https://img.shields.io/badge/MATLAB-Simulation-blue)
![Physics](https://img.shields.io/badge/Computational-Physics-orange)
![Numerical Methods](https://img.shields.io/badge/Numerical-Methods-success)

**Laplace 3D Explorer** adalah aplikasi berbasis MATLAB untuk menyelesaikan dan memvisualisasikan distribusi temperatur tiga dimensi. Aplikasi ini dirancang sebagai alat pembelajaran Numerical Methods dan Computational Physics dengan memberikan pengalaman visual interaktif yang menyerupai CT Scan atau MRI Viewer.

---

## Project Overview

Tujuan utama proyek ini adalah memungkinkan pengguna untuk mengeksplorasi distribusi temperatur dalam volume 3D secara interaktif. Solver dibangun untuk menyelesaikan Persamaan Laplace menggunakan beberapa metode numerik:
* **Finite Difference Method (FDM)**
* **Gauss-Seidel Method**
* **Successive Over Relaxation (SOR)**

## Mathematical Background

Aplikasi ini menyelesaikan persamaan Laplace 3D:

$$ \nabla^2 T = 0 $$

atau dalam bentuk diferensial parsial:

$$ \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} + \frac{\partial^2 T}{\partial z^2} = 0 $$

Diskretisasi menggunakan Finite Difference:

$$ T_{i,j,k} = \frac{T_{i+1,j,k} + T_{i-1,j,k} + T_{i,j+1,k} + T_{i,j-1,k} + T_{i,j,k+1} + T_{i,j,k-1}}{6} $$

Iterasi menggunakan metode SOR (Successive Over Relaxation):

$$ T^{new} = T^{old} + \omega (T_{GS}-T^{old}) $$

## Project Goals

### Educational Goals
Pengguna diharapkan dapat memahami konsep-konsep berikut secara mendalam:
- Persamaan Laplace & Finite Difference Method
- Grid 3D & Boundary Condition
- Iterative Solver (Gauss-Seidel, SOR)
- Konvergensi Iteratif & Error Analysis

### Technical Goals
Membangun aplikasi yang:
- Modular, mudah dikembangkan, dan mudah dipelihara.
- Memisahkan secara jelas antara Layer GUI, Visualization, Solver, dan Mathematical Core.
- Dapat diperluas untuk Heat Equation dan Poisson Equation di masa depan.

## Target Users
- Mahasiswa Fisika, Teknik Elektro, Mesin, dan Sipil
- Enthusiast Computational Physics & Pembelajar Numerical Methods

## System Architecture

Arsitektur aplikasi dirancang modular agar Solver independen dari GUI, dan Visualisasi tidak melakukan kalkulasi numerik.

```text
GUI Layer
    ↓
Visualization Layer
    ↓
Solver Layer
    ↓
Mathematical Core
```

### Folder Structure

```text
Laplace3DExplorer/
├── main.m
├── solver/
│   └── solver3D.m
├── visualization/
│   ├── showHeatmap.m
│   ├── showContour.m
│   ├── showSurface.m
│   ├── showScatter3D.m
│   ├── showSlice3D.m
│   └── showIsosurface.m
├── gui/
│   └── Laplace3DExplorer.mlapp
└── docs/
```

## Features & Roadmap

Aplikasi dikembangkan dalam berbagai fase yang mencakup:
- **Numerical Core**: Domain/Grid Generation, Boundary Conditions, SOR Solver, Error Calculation.
- **2D/3D Visualization**: Heatmap, Contour, Surface, Scatter Volume, Slice Volume, Isosurface.
- **CT Scan & Orthogonal Viewer**: Navigasi layer-by-layer (Z Layer) dan tampilan 3 arah (XY, XZ, YZ Plane).
- **Interactive Boundary Conditions**: Ubah nilai batas (Kiri, Kanan, Depan, Belakang, Atas, Bawah) secara real-time.
- **Simulation Control Panel**: Kontrol Grid Size, Omega ($\omega$), Tolerance, dan Max Iterations.
- **Scientific Dashboard**: Metrik seperti iterasi, residual error, suhu minimum/maksimum/rata-rata/pusat.
- **Data Export**: Ekspor visualisasi ke PNG/JPG dan data ke CSV/MAT.

## Future Extensions

Aplikasi ini diproyeksikan untuk menjadi fondasi bagi simulator fisika yang lebih kompleks, seperti:
- **Heat Equation Solver** ($\frac{\partial T}{\partial t} = \alpha \nabla^2 T$)
- **Poisson Equation Solver** ($\nabla^2 T = f(x,y,z)$)
- **Electrostatic Potential Solver** ($\nabla^2 V = 0$)
- **Diffusion Simulation & Mini COMSOL-Style Simulator**

## Coding Standards
- Mengutamakan *Modular Functions* dan *Single Responsibility Principle*.
- Memisahkan fungsionalitas Solver dan Visualization.
- Menggunakan praktik terbaik MATLAB untuk performa dan skalabilitas kode.
