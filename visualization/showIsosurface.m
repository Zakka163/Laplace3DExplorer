function showIsosurface(X, Y, Z, T)
    fig = figure('Name', '3D Isosurface', 'Color', [0.1 0.1 0.1]);
    ax = axes('Parent', fig);
    
    iso_val = (min(T(:)) + max(T(:))) / 2;
    
    [faces, verts] = isosurface(X, Y, Z, T, iso_val);
    p = patch(ax, 'Vertices', verts, 'Faces', faces, 'FaceColor', 'r', 'EdgeColor', 'none');
    isonormals(X, Y, Z, T, p);
    
    camlight(ax);
    lighting(ax, 'gouraud');
    
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w', 'GridColor', 'w');
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold'); 
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold'); 
    zlabel(ax, 'Z', 'Color', 'w', 'FontWeight', 'bold');
    title(ax, sprintf('Isosurface (T = %.2f)', iso_val), 'Color', 'w', 'FontWeight', 'bold');
    
    view(ax, 3);
    grid(ax, 'on');
    axis(ax, 'equal', 'tight');
end
