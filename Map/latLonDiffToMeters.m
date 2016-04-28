function [meters] = latLonDiffToMeters(lat1, lon1, lat2, lon2)  % generally used geo measurement function
    R = 6378.137; % Radius of earth in KM
    dLat = (lat2 - lat1) * Math.PI / 180;
    dLon = (lon2 - lon1) * Math.PI / 180;
    
    a = Math.sin(dLat/2) * Math.sin(dLat/2) + ...
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * ...
        Math.sin(dLon/2) * Math.sin(dLon/2);
    
    c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    meters = R * c * 1000; % cm -> meters
end