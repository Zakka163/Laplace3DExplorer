<div align="center">
  <h1>Laplace 3D Explorer</h1>
  <p><b>A High-Performance MATLAB Solver & Scientific Visualization Tool for 3D Heat Distribution</b></p>
  
  [![MATLAB](https://img.shields.io/badge/Made_with-MATLAB-blue.svg)](https://www.mathworks.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
  [![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()
</div>

<br/>

## Overview

**Laplace 3D Explorer** is a robust, modular, and interactive MATLAB application designed to solve the 3D Laplace equation ($\nabla^2 T = 0$) using high-performance numerical methods. It acts as a "Mini COMSOL" specifically tailored for educational and computational physics purposes. 

Featuring a fully integrated Graphical User Interface (GUI), the software allows researchers and students to configure boundary conditions, execute the Successive Over-Relaxation (SOR) solver, and instantly render breathtaking volumetric visualizations comparable to CT Scan or MRI viewers.

---

## Key Features

- **Optimized Numerical Core**: Uses an efficient class-based 3D Solver utilizing the SOR (Successive Over-Relaxation) algorithm capable of handling millions of grid nodes seamlessly.
- **Interactive Programmatic GUI**: No coding required! A clean, single-window application built natively using `uifigure` to control boundaries and solver parameters in real-time.
- **Scientific Dashboard**: Live metrics tracking including calculation time, convergence error, iteration count, and absolute temperature extremes.
- **Advanced 3D Volumetric Visualization**: Includes a rich suite of visual modes:
  - `Orthogonal Viewer` & `Slice 3D`: Navigate through Z/Y/X layers just like medical imaging software.
  - `Isosurface 3D`: Renders dynamic temperature-boundary shells with Gouraud lighting.
  - `Scatter 3D`: Plots thermal point clouds with automated memory-safe downsampling.
  - `Heatmap` & `Contour`: Classic 2D mid-plane projections.
- **Data Export**: Save thermal arrays to `.csv`, `.mat`, or render high-resolution `.png` graphics with a single click.

---

## Getting Started

### Prerequisites
- **MATLAB R2020b or newer** (Recommended for `uifigure` and `uigridlayout` full support).

### Installation & Launch
1. Clone this repository or extract the project folder.
2. Open MATLAB and navigate to the project's root directory (`Laplace3DExplorer`).
3. To launch the GUI application, simply type the following command in the **Command Window**:
   ```matlab
   runApp
   ```
4. The Laplace 3D Explorer interface will launch instantly!

---

## Mathematical Background

The application solves the steady-state heat equation (Laplace's equation) in three dimensions:

$$ \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} + \frac{\partial^2 T}{\partial z^2} = 0 $$

We discretize the domain using the **Finite Difference Method**:

$$ T_{i,j,k} = \frac{T_{i+1,j,k} + T_{i-1,j,k} + T_{i,j+1,k} + T_{i,j-1,k} + T_{i,j,k+1} + T_{i,j,k-1}}{6} $$

To dramatically accelerate convergence on massive grids (e.g. 8+ million nodes), the solver implements the **Successive Over-Relaxation (SOR)** algorithm:

$$ T^{new} = T^{old} + \omega (T_{GS}-T^{old}) $$

Where $\omega$ is the relaxation factor (typically between $1.0$ and $2.0$).

---

## Architecture & Directory Structure

The project strictly adheres to **Clean Code** principles and the **Single Responsibility Principle**. 

```text
Laplace3DExplorer/
├── runApp.m                  # App launcher script
├── main.m                    # Headless benchmarking & testing script
├── gui/
│   └── Laplace3DApp.m        # The unified programmatic GUI class
├── solver/
│   └── solver3D.m            # The core numerical object-oriented solver
└── visualization/            # Modular plotting engines
    ├── orthogonalViewer.m
    ├── showContour.m
    ├── showHeatmap.m
    ├── showIsosurface.m
    ├── showScatter3D.m
    ├── showSlice3D.m
    ├── showSurface.m
    └── sliceViewer.m
```

---

## Future Extensions
The modular foundation of Laplace 3D Explorer is specifically designed to be easily expanded into:
- **Heat Equation Solvers** (Time-dependent diffusion $\frac{\partial T}{\partial t} = \alpha \nabla^2 T$)
- **Poisson Equation Solvers** (Internal heat generation $\nabla^2 T = f(x,y,z)$)
- **Electrostatics** (Electric potential simulations $\nabla^2 V = 0$)

---

## License
This project is open-source and free to use for academic, research, and educational purposes.
