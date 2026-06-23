classdef Laplace3DApp < handle
    properties
        UIFigure
        GridLayout
        LeftPanel
        CenterPanel
        RightPanel
        
        % Inputs
        EditLeft, EditRight, EditFront, EditBack, EditBottom, EditTop
        EditDx, EditMaxIter, EditTol, EditOmega
        
        % Visuals
        UIAxes
        VisDropdown
        ZSlider
        
        % Dashboard Labels
        LblIter, LblErr, LblTime, LblMaxT, LblMinT, LblCenterT
        
        % Data
        T, X, Y, Z
    end
    
    methods
        function obj = Laplace3DApp()
            addpath('solver');
            addpath('visualization');
            obj.buildUI();
        end
        
        function buildUI(obj)
            obj.UIFigure = uifigure('Name', 'Laplace 3D Explorer', 'Position', [100 100 1200 700], 'Color', [0.12 0.12 0.12]);
            obj.GridLayout = uigridlayout(obj.UIFigure, [1 3]);
            obj.GridLayout.ColumnWidth = {280, '1x', 250};
            obj.GridLayout.BackgroundColor = [0.12 0.12 0.12];
            
            % --- LEFT PANEL ---
            obj.LeftPanel = uipanel(obj.GridLayout, 'Title', 'Control Panel', 'BackgroundColor', [0.15 0.15 0.15], 'ForegroundColor', 'w');
            leftGrid = uigridlayout(obj.LeftPanel, [12 2]);
            leftGrid.RowHeight = {22, 22, 22, 22, 22, 22, 22, 22, 22, 22, '1x', 40};
            leftGrid.BackgroundColor = [0.15 0.15 0.15];
            
            obj.EditLeft = obj.addInput(leftGrid, 'BC Left:', 100);
            obj.EditRight = obj.addInput(leftGrid, 'BC Right:', 50);
            obj.EditFront = obj.addInput(leftGrid, 'BC Front:', 0);
            obj.EditBack = obj.addInput(leftGrid, 'BC Back:', 100);
            obj.EditBottom = obj.addInput(leftGrid, 'BC Bottom:', 75);
            obj.EditTop = obj.addInput(leftGrid, 'BC Top:', 25);
            
            obj.EditDx = obj.addInput(leftGrid, 'Grid dx:', 0.05);
            obj.EditOmega = obj.addInput(leftGrid, 'Omega:', 1.8);
            obj.EditTol = obj.addInput(leftGrid, 'Tolerance:', 1e-6);
            obj.EditMaxIter = obj.addInput(leftGrid, 'Max Iter:', 2000);
            
            btnSolve = uibutton(leftGrid, 'Text', 'SOLVE', 'BackgroundColor', [0 0.5 0], 'FontColor', 'w', 'FontWeight', 'bold');
            btnSolve.Layout.Row = 12; btnSolve.Layout.Column = [1 2];
            btnSolve.ButtonPushedFcn = @(~, ~) obj.solveSystem();
            
            % --- CENTER PANEL ---
            obj.CenterPanel = uipanel(obj.GridLayout, 'Title', 'Visualization', 'BackgroundColor', [0.1 0.1 0.1], 'ForegroundColor', 'w');
            centerGrid = uigridlayout(obj.CenterPanel, [2 1]);
            centerGrid.RowHeight = {45, '1x'};
            centerGrid.BackgroundColor = [0.1 0.1 0.1];
            
            topCenter = uigridlayout(centerGrid, [1 4]);
            topCenter.ColumnWidth = {80, 160, 60, '1x'};
            topCenter.Padding = [0 5 0 5];
            topCenter.BackgroundColor = [0.1 0.1 0.1];
            uilabel(topCenter, 'Text', 'Visual Type:', 'FontColor', 'w');
            obj.VisDropdown = uidropdown(topCenter, 'Items', {'Heatmap 2D', 'Contour 2D', 'Surface 2D', 'Scatter 3D', 'Slice 3D', 'Isosurface'});
            obj.VisDropdown.ValueChangedFcn = @(~, ~) obj.renderVisualization();
            
            uilabel(topCenter, 'Text', 'Z Layer:', 'FontColor', 'w');
            obj.ZSlider = uislider(topCenter, 'Limits', [1 10], 'Value', 5);
            obj.ZSlider.ValueChangedFcn = @(~, ~) obj.renderVisualization();
            obj.ZSlider.FontColor = 'w';
            
            obj.UIAxes = uiaxes(centerGrid);
            obj.UIAxes.Color = 'k'; obj.UIAxes.XColor = 'w'; obj.UIAxes.YColor = 'w'; obj.UIAxes.ZColor = 'w';
            
            % --- RIGHT PANEL ---
            obj.RightPanel = uipanel(obj.GridLayout, 'Title', 'Dashboard & Export', 'BackgroundColor', [0.15 0.15 0.15], 'ForegroundColor', 'w');
            rightGrid = uigridlayout(obj.RightPanel, [10 1]);
            rightGrid.RowHeight = {22, 22, 22, 22, 22, 22, '1x', 30, 30, 30};
            rightGrid.BackgroundColor = [0.15 0.15 0.15];
            
            obj.LblTime = obj.addLabel(rightGrid, 'Time: - s');
            obj.LblIter = obj.addLabel(rightGrid, 'Iter: -');
            obj.LblErr = obj.addLabel(rightGrid, 'Error: -');
            obj.LblMaxT = obj.addLabel(rightGrid, 'Max Temp: -');
            obj.LblMinT = obj.addLabel(rightGrid, 'Min Temp: -');
            obj.LblCenterT = obj.addLabel(rightGrid, 'Center Temp: -');
            
            btnPNG = uibutton(rightGrid, 'Text', 'Save PNG', 'ButtonPushedFcn', @(~,~) obj.exportData('png'));
            btnCSV = uibutton(rightGrid, 'Text', 'Export CSV', 'ButtonPushedFcn', @(~,~) obj.exportData('csv'));
            btnMAT = uibutton(rightGrid, 'Text', 'Export MAT', 'ButtonPushedFcn', @(~,~) obj.exportData('mat'));
        end
        
        function editField = addInput(~, parent, lblText, defaultVal)
            uilabel(parent, 'Text', lblText, 'FontColor', 'w');
            editField = uieditfield(parent, 'numeric', 'Value', defaultVal);
        end
        
        function lbl = addLabel(~, parent, lblText)
            lbl = uilabel(parent, 'Text', lblText, 'FontColor', 'w', 'FontWeight', 'bold');
        end
        
        function solveSystem(obj)
            BC.left = obj.EditLeft.Value; BC.right = obj.EditRight.Value;
            BC.front = obj.EditFront.Value; BC.back = obj.EditBack.Value;
            BC.bottom = obj.EditBottom.Value; BC.top = obj.EditTop.Value;
            
            dx = obj.EditDx.Value;
            omega = obj.EditOmega.Value;
            tol = obj.EditTol.Value;
            maxIter = obj.EditMaxIter.Value;
            
            obj.UIFigure.Name = 'Laplace 3D Explorer - SOLVING...';
            drawnow;
            
            tic;
            s = solver3D(1.0, 1.0, 1.0, dx, BC, 'sor', omega, tol, maxIter);
            s = s.solve();
            elapsed = toc;
            
            obj.T = s.T; obj.X = s.X; obj.Y = s.Y; obj.Z = s.Z;
            
            obj.LblTime.Text = sprintf('Time: %.3f s', elapsed);
            obj.LblIter.Text = sprintf('Iter: %d', s.iter);
            obj.LblErr.Text = sprintf('Error: %e', s.err);
            obj.LblMaxT.Text = sprintf('Max Temp: %.2f', max(s.T(:)));
            obj.LblMinT.Text = sprintf('Min Temp: %.2f', min(s.T(:)));
            
            mid_y = round(size(s.T, 1) / 2);
            mid_x = round(size(s.T, 2) / 2);
            mid_z = round(size(s.T, 3) / 2);
            obj.LblCenterT.Text = sprintf('Center Temp: %.2f', s.T(mid_y, mid_x, mid_z));
            
            nz = size(s.T, 3);
            obj.ZSlider.Limits = [1 nz];
            obj.ZSlider.Value = mid_z;
            obj.ZSlider.MajorTicks = [1 mid_z nz];
            
            obj.UIFigure.Name = 'Laplace 3D Explorer';
            obj.renderVisualization();
        end
        
        function renderVisualization(obj)
            if isempty(obj.T), return; end
            
            cla(obj.UIAxes);
            ax = obj.UIAxes;
            type = obj.VisDropdown.Value;
            
            curr_z = round(obj.ZSlider.Value);
            X2D = obj.X(:, :, curr_z); Y2D = obj.Y(:, :, curr_z); T2D = obj.T(:, :, curr_z);
            
            switch type
                case 'Heatmap 2D'
                    imagesc(ax, X2D(1,:), Y2D(:,1), T2D);
                    set(ax, 'YDir', 'normal'); axis(ax, 'equal', 'tight');
                    view(ax, 2);
                case 'Contour 2D'
                    contourf(ax, X2D, Y2D, T2D, 20, 'LineColor', 'none');
                    axis(ax, 'equal', 'tight');
                    view(ax, 2);
                case 'Surface 2D'
                    surf(ax, X2D, Y2D, T2D, 'EdgeColor', 'none');
                    view(ax, 3);
                case 'Scatter 3D'
                    step = ceil(numel(obj.T) / 5000);
                    scatter3(ax, obj.X(1:step:end), obj.Y(1:step:end), obj.Z(1:step:end), 10, obj.T(1:step:end), 'filled');
                    view(ax, 3);
                case 'Slice 3D'
                    mx = obj.X(1, round(size(obj.X,2)/2), 1);
                    my = obj.Y(round(size(obj.Y,1)/2), 1, 1);
                    mz = obj.Z(1, 1, round(size(obj.Z,3)/2));
                    h = slice(ax, obj.X, obj.Y, obj.Z, obj.T, mx, my, mz);
                    set(h, 'EdgeColor', 'none', 'FaceAlpha', 0.8);
                    view(ax, 3);
                case 'Isosurface'
                    val = (min(obj.T(:)) + max(obj.T(:))) / 2;
                    [f, v] = isosurface(obj.X, obj.Y, obj.Z, obj.T, val);
                    p = patch(ax, 'Vertices', v, 'Faces', f, 'FaceColor', 'r', 'EdgeColor', 'none');
                    isonormals(obj.X, obj.Y, obj.Z, obj.T, p);
                    view(ax, 3);
            end
            colormap(ax, 'jet');
            grid(ax, 'on');
        end
        
        function exportData(obj, type)
            if isempty(obj.T), return; end
            switch type
                case 'png'
                    exportgraphics(obj.UIAxes, 'Laplace3D_Export.png', 'Resolution', 300);
                case 'csv'
                    mid_z = round(size(obj.T, 3) / 2);
                    csvwrite('Laplace3D_MidZ_Export.csv', obj.T(:,:,mid_z));
                case 'mat'
                    T = obj.T; X = obj.X; Y = obj.Y; Z = obj.Z;
                    save('Laplace3D_Export.mat', 'T', 'X', 'Y', 'Z');
            end
            uialert(obj.UIFigure, ['Export ' upper(type) ' sukses! File tersimpan di folder aktif.'], 'Export Data');
        end
    end
end
