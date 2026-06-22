function showSurface(X2D, Y2D, T2D, ax)
    if nargin < 4 || isempty(ax)
        figure('Name', 'Surface XY', 'Color', 'w');
        ax = gca;
    end
    
    surf(ax, X2D, Y2D, T2D, 'EdgeColor', 'none');
    
    colorbar(ax);
    colormap(ax, 'jet');
    xlabel(ax, 'X');
    ylabel(ax, 'Y');
    zlabel(ax, 'Temperature');
    title(ax, 'Temperature Surface 3D');
    
    view(ax, 3);
    grid(ax, 'on');
end
