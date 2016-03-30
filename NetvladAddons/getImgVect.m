function [ features ] = getImgVect( img_dir, img_names, output_path )
display('Setting up environment vars')
% Set the MATLAB paths
setup;
num_images = size(img_names,1);
display('Loading network into memory')
% Load NetVLAD
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

display('Calculating feature vectors')
% Calculate all the vectors
serialAllFeats(net, img_dir, img_names, output_path, 'batchSize', 1);

display('Reshaping feature vectors to matrix form')
dbFeat= fread( fopen(output_path, 'rb'), inf, 'float32=>single');
dbFeat= reshape(dbFeat, [], num_images);
features = dbFeat

end
