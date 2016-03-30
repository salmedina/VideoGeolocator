function fileList = getFileList(dirName)
  dirName = strcat(dirName,'/*.jpg')
  dirData = dir(dirName);      %# Get the data for the current directory
  dirIndex = [dirData.isdir];  %# Find the index for directories
  fileList = {dirData(~dirIndex).name}';  %'# Get a list of the files
  if ~isempty(fileList)
    fileList = cellfun(@(x) x,...  %# Prepend path to files
                       fileList,'UniformOutput',false);
  end
end