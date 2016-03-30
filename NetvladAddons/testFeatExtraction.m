frames_dir = '/Users/zal/CMU/Spring2016/11775/Project/netvlad/analysis/VideoTest/keyframes/te'
frames_names = getFileList(frames_dir)
output_path = fullfile(frames_dir, 'feats.bin')
feats = getImgVect(frames_dir, frames_names, output_path)