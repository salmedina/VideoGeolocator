function [ ] = strCellArrToTxt( strCellArr , outputPath)
% Save each element of a string list per line into txt file

fileID = fopen(outputPath,'w');
for i = 1:numel(strCellArr)
    outLine = sprintf('%s\n',strCellArr{i});
    fprintf(fileID, outLine);
end
fclose(fileID);

end

