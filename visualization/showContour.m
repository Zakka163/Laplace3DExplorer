function showContour(X2D, Y2D, T2D, ax)
    if nargin < 4 || isempty(ax)
        figure('Name', 'Contour XY', 'Color', 'w');
        ax = gca;
    end
    
    contourf(ax, X2D, Y2D, T2D, 25, 'LineColor', 'none');
    axis(ax, 'equal', 'tight');
    
    colorbar(ax);
    colormap(ax, 'jet');
    xlabel(ax, 'X');
    ylabel(ax, 'Y');
    title(ax, 'Temperature Contour');
end
