function [ ] = getImgVect( img_dir, img_names, out_dir, batch_size)
%preprocess arguments
if ischar(batch_size)
    batch_size = str2num(batch_size);
end

% Set the MATLAB paths
display('Setting up environment vars')
setup;

% Load NetVLAD
display('Loading network into memory')
netID= 'vd16_pitts30k_conv5_3_vlad_preL2_intra_white';
paths= localPaths();
load( sprintf('%s%s.mat', paths.ourCNNs, netID), 'net' );
net= relja_simplenn_tidy(net);

% Relies on the fact that NetVLAD, Max and Avg pooling are implemented as a 
% custom layer and are the first custom layer in the network. 
% Change if you use another network which has other custom layers before
lastConvLayer= find(ismember(relja_layerTypes(net), 'custom'),1)-1; 
netBottom=net;
netBottom.layers=netBottom.layers(1:lastConvLayer);
info= vl_simplenn_display(netBottom);
clear netBottom;
recFieldSize= info.receptiveFieldSize(:, end);
% we are assuming square receptive fields, otherwise dbVGG needs to change to 
% account for non-square
assert(recFieldSize(1) == recFieldSize(2));
recFieldSize= recFieldSize(1);
strMode= 'crop';

% Calculate all the vectors
display('Calculating feature vectors')
num_images = length(img_names);
batchIdxList = 1:batch_size:num_images;
tmpOutPath = fullfile(out_dir, 'tmp.bin');

tStart = tic;  % Start time of batch processing
curBatchPos = 1;
numBatches = length(batchIdxList);
for curIdx = batchIdxList
    tBatchStart = tic;
    display(sprintf('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Processing batch %d / %d',...
                    curBatchPos, numBatches));
    
    if curIdx == batchIdxList(end)
        batchEndIdx = num_images;
    else
        batchEndIdx = curIdx+batch_size- 1;
    end
    curBatchSz = batchEndIdx - curIdx + 1;
    
    % Compute the batch features, feats are stored in tmp bin file
    imgSubset = img_names(curIdx:batchEndIdx);
    serialAllFeats(net, img_dir, imgSubset, tmpOutPath, 'batchSize', curBatchSz);
    
    %Load tmp binary file into matlab matrix
    display('Reshaping feature vectors to matrix form')
    fileHandle = fopen(tmpOutPath, 'rb');
    batchFeats= fread( fileHandle, inf, 'float32=>single');
    fclose(fileHandle);
    batchFeats= reshape(batchFeats, [], curBatchSz);
    
    %save feat vectors into file
    batchMatNameStr = sprintf('Batch_%d_%d.mat', curIdx, batchEndIdx);    
    batchMatPath = fullfile(out_dir, batchMatNameStr);
    save(batchMatPath, 'batchFeats');
    display(sprintf('Saved feats file %s',batchMatNameStr));

    %Save file name list into txt file in same order as the vectors are
    %stored
    batchTxtNameStr = sprintf('Batch_%d_%d.txt', curIdx, batchEndIdx);
    batchTxtPath = fullfile(out_dir, batchTxtNameStr);
    strCellArrToTxt(img_names(curIdx:batchEndIdx), batchTxtPath);
        display(sprintf('Saved names file %s',batchTxtNameStr));
        
    % Display vars    
    batchExecTime = toc(tBatchStart)/86400;
    avgExecTime   = toc(tStart)/(86400*curBatchPos);
    if curBatchPos >= numBatches
        remApproxTime = 0;
    else
        remApproxTime = avgExecTime * (numBatches-curBatchPos);
    end
    
    batchExecTimeStr = datestr(batchExecTime, 'HH:MM:SS.FFF');
    avgExecTimeStr   = datestr(avgExecTime,     'HH:MM:SS.FFF');
    remApproxTimeStr = datestr(remApproxTime, 'HH:MM:SS.FFF');
    
    display(sprintf('Batch proceesing time:   %s',batchExecTimeStr));
    display(sprintf('Avg proceesing time:     %s',avgExecTimeStr));
    display(sprintf('Approx. remaining time:  %s',remApproxTimeStr));
    
    curBatchPos    = curBatchPos + 1;
end

end