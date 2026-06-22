function showHeatmap(X2D, Y2D, T2D, ax)
    if nargin < 4 || isempty(ax)
        fig = figure('Name', 'Heatmap XY', 'Color', [0.1 0.1 0.1]); 
        ax = axes('Parent', fig);
    end
    
    imagesc(ax, X2D(1,:), Y2D(:,1), T2D);
    set(ax, 'YDir', 'normal');
    axis(ax, 'equal', 'tight');
    
    cb = colorbar(ax);
    cb.Color = 'w';
    colormap(ax, 'jet');
    
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w');
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold');
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold');
    title(ax, 'Temperature Heatmap', 'Color', 'w', 'FontSize', 12);
end
