function showSurface(X2D, Y2D, T2D, ax)
    if nargin < 4 || isempty(ax)
        fig = figure('Name', 'Surface XY', 'Color', [0.1 0.1 0.1]);
        ax = axes('Parent', fig);
    end
    
    surf(ax, X2D, Y2D, T2D, 'EdgeColor', 'none');
    
    cb = colorbar(ax);
    cb.Color = 'w';
    colormap(ax, 'jet');
    
    % Styling
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w', 'GridColor', 'w', 'GridAlpha', 0.4);
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold');
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold');
    zlabel(ax, 'Temperature', 'Color', 'w', 'FontWeight', 'bold');
    title(ax, 'Temperature Surface 3D', 'Color', 'w', 'FontSize', 12);
    
    view(ax, 3);
    grid(ax, 'on');
end
