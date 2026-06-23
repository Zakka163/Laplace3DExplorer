function showScatter3D(X, Y, Z, T)
    fig = figure('Name', '3D Scatter Volume', 'Color', [0.1 0.1 0.1]);
    ax = axes('Parent', fig);
    
    max_pts = 10000;
    total_pts = numel(T);
    step = ceil(total_pts / max_pts);
    
    Xs = X(1:step:end);
    Ys = Y(1:step:end);
    Zs = Z(1:step:end);
    Ts = T(1:step:end);
    
    scatter3(ax, Xs, Ys, Zs, 15, Ts, 'filled', 'MarkerFaceAlpha', 0.6);
    
    colormap(ax, 'jet');
    cb = colorbar(ax);
    cb.Color = 'w';
    
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w', 'GridColor', 'w');
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold'); 
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold'); 
    zlabel(ax, 'Z', 'Color', 'w', 'FontWeight', 'bold');
    title(ax, '3D Scatter Temperature', 'Color', 'w', 'FontWeight', 'bold');
    
    view(ax, 3);
    grid(ax, 'on');
    axis(ax, 'equal', 'tight');
end
