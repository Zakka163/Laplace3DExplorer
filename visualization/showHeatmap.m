function showHeatmap(X2D, Y2D, T2D, ax)
    if nargin < 4 || isempty(ax)
        figure('Name', 'Heatmap XY', 'Color', 'w');
        ax = gca;
    end
    
    imagesc(ax, X2D(1,:), Y2D(:,1), T2D);
    set(ax, 'YDir', 'normal');
    axis(ax, 'equal', 'tight');
    
    colorbar(ax);
    colormap(ax, 'jet');
    xlabel(ax, 'X');
    ylabel(ax, 'Y');
    title(ax, 'Temperature Heatmap');
end
