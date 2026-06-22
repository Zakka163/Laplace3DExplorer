function showContour(X2D, Y2D, T2D, ax)
    if nargin < 4 || isempty(ax)
        fig = figure('Name', 'Contour XY', 'Color', [0.1 0.1 0.1]);
        ax = axes('Parent', fig);
    end
    
    contourf(ax, X2D, Y2D, T2D, 25, 'LineColor', 'none');
    axis(ax, 'equal', 'tight');
    
    cb = colorbar(ax);
    cb.Color = 'w';
    colormap(ax, 'jet');
    
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w');
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold');
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold');
    title(ax, 'Temperature Contour', 'Color', 'w', 'FontSize', 12);
end
