function [] = runFeatExtraction(img_dir, output_dir, batch_size)
    % Display title and input arguments
    display('>>>>>>>>>>>>   Extracting NetVLAD Features <<<<<<<<<<<<<<');
    cur_dir = pwd;
    display(sprintf('Current Dir:  %s', cur_dir));
    display(sprintf('Image Dir:    %s', img_dir));
    display(sprintf('Output Dir:   %s', output_dir));
    display(sprintf('Batch Size:   %s', batch_size));
    
    img_names = getFileList(img_dir, '.jpg'); %returns a str cell array
    num_images = numel(img_names);    
    if num_images > 0
        % Images were found in folder
        display(sprintf('%d image files were found.\n', num_images));
        getImgVect(img_dir, img_names, output_dir, batch_size);
    else
        % No images were found in folder
        display('No images were found in the directory');
    end
end