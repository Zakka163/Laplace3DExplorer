function showSlice3D(X, Y, Z, T)
    fig = figure('Name', '3D Slice Volume', 'Color', [0.1 0.1 0.1]);
    ax = axes('Parent', fig);
    
    mid_x = X(1, round(size(X,2)/2), 1);
    mid_y = Y(round(size(Y,1)/2), 1, 1);
    mid_z = Z(1, 1, round(size(Z,3)/2));
    
    h = slice(ax, X, Y, Z, T, mid_x, mid_y, mid_z);
    set(h, 'EdgeColor', 'none', 'FaceAlpha', 0.8);
    
    colormap(ax, 'jet');
    cb = colorbar(ax);
    cb.Color = 'w';
    
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w', 'GridColor', 'w');
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold'); 
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold'); 
    zlabel(ax, 'Z', 'Color', 'w', 'FontWeight', 'bold');
    title(ax, 'Orthogonal Slices in 3D', 'Color', 'w', 'FontWeight', 'bold');
    
    view(ax, 3);
    grid(ax, 'on');
    axis(ax, 'equal', 'tight');
end
