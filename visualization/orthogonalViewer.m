function orthogonalViewer(X, Y, Z, T)
    fig = figure('Name', 'Orthogonal Viewer', 'Color', [0.1 0.1 0.1], ...
                 'Position', [150, 150, 800, 600]);

    nx = size(T, 2);
    ny = size(T, 1);
    nz = size(T, 3);
    
    mid_x = round(nx / 2);
    mid_y = round(ny / 2);
    mid_z = round(nz / 2);

    global_min = min(T(:));
    global_max = max(T(:));

    ax1 = subplot(2, 2, [1 2], 'Parent', fig);
    imagesc(ax1, X(1,:,1), Y(:,1,1), T(:,:,mid_z));
    set(ax1, 'YDir', 'normal', 'Color', 'k', 'XColor', 'w', 'YColor', 'w');
    axis(ax1, 'equal', 'tight');
    title(ax1, sprintf('XY Plane (Z = %.2f)', Z(1,1,mid_z)), 'Color', 'w', 'FontWeight', 'bold');
    xlabel(ax1, 'X', 'Color', 'w'); ylabel(ax1, 'Y', 'Color', 'w');
    caxis(ax1, [global_min global_max]);

    ax2 = subplot(2, 2, 3, 'Parent', fig);
    xz_slice = squeeze(T(mid_y, :, :))';
    imagesc(ax2, X(1,:,1), squeeze(Z(1,1,:)), xz_slice);
    set(ax2, 'YDir', 'normal', 'Color', 'k', 'XColor', 'w', 'YColor', 'w');
    axis(ax2, 'equal', 'tight');
    title(ax2, sprintf('XZ Plane (Y = %.2f)', Y(mid_y,1,1)), 'Color', 'w', 'FontWeight', 'bold');
    xlabel(ax2, 'X', 'Color', 'w'); ylabel(ax2, 'Z', 'Color', 'w');
    caxis(ax2, [global_min global_max]);

    ax3 = subplot(2, 2, 4, 'Parent', fig);
    yz_slice = squeeze(T(:, mid_x, :))';
    imagesc(ax3, Y(:,1,1), squeeze(Z(1,1,:)), yz_slice);
    set(ax3, 'YDir', 'normal', 'Color', 'k', 'XColor', 'w', 'YColor', 'w');
    axis(ax3, 'equal', 'tight');
    title(ax3, sprintf('YZ Plane (X = %.2f)', X(1,mid_x,1)), 'Color', 'w', 'FontWeight', 'bold');
    xlabel(ax3, 'Y', 'Color', 'w'); ylabel(ax3, 'Z', 'Color', 'w');
    caxis(ax3, [global_min global_max]);

    colormap(fig, 'jet');
end
