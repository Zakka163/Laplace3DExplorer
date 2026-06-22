function sliceViewer(X, Y, Z, T)
    fig = figure('Name', 'CT Scan Viewer - Z Layers', 'Color', [0.1 0.1 0.1], ...
                 'Position', [100, 100, 700, 600]);
    
    ax = axes('Parent', fig, 'Position', [0.1, 0.2, 0.8, 0.7]);
    
    nz = size(T, 3);
    current_z = round(nz / 2);
    
    img = imagesc(ax, X(1,:,1), Y(:,1,1), T(:,:,current_z));
    set(ax, 'YDir', 'normal');
    axis(ax, 'equal', 'tight');
    
    cb = colorbar(ax);
    cb.Color = 'w';
    colormap(ax, 'jet');
    caxis(ax, [min(T(:)), max(T(:))]); 
    
    set(ax, 'Color', 'k', 'XColor', 'w', 'YColor', 'w');
    xlabel(ax, 'X', 'Color', 'w', 'FontWeight', 'bold');
    ylabel(ax, 'Y', 'Color', 'w', 'FontWeight', 'bold');
    
    title_text = title(ax, sprintf('Z-Layer: %d / %d (Z = %.2f)', current_z, nz, Z(1,1,current_z)), ...
                       'Color', 'w', 'FontSize', 12);
    
    slider = uicontrol('Parent', fig, 'Style', 'slider', ...
                       'Units', 'normalized', 'Position', [0.1, 0.05, 0.8, 0.05], ...
                       'Min', 1, 'Max', nz, 'Value', current_z, ...
                       'SliderStep', [1/(max(1, nz-1)), max(1/(max(1, nz-1)), 0.1)]);
                   
    addlistener(slider, 'Value', 'PostSet', @(~,~) updateSlice());
    
    function updateSlice()
        idx = round(slider.Value);
        img.CData = T(:,:,idx);
        title_text.String = sprintf('Z-Layer: %d / %d (Z = %.2f)', idx, nz, Z(1,1,idx));
    end
end
