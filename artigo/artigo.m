% Accuracy Sensitivity Precision F-Measure G-mean AUC
clear;

% Example data as before
model_series = [10 40 50 60; 20 50 60 70; 30 60 80 90; 10 20 30 40];
model_error = [1 4 8 6; 2 5 9 12; 3 6 10 13; 5 10 12 40];
b = bar(model_series, 'grouped');

%% For MATLAB R2019a or earlier releases
hold on

% Find the number of groups and the number of bars in each group
% ngroups = size(model_series, 1);
% nbars = size(model_series, 2);
[ngroups, nbars] = size(model_series);


% Calculate the width for each bar group
groupwidth = min(0.8, nbars/(nbars + 1.5));

% Set the position of each error bar in the centre of the main bar
% Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange
for i = 1:nbars
    % Calculate center of each bar
    x = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
    
    errorbar(x, model_series(:, i), model_error(:, i), 'k', 'linestyle', 'none');
end

hold off

%% For MATLAB 2019b or later releases
hold on

% Calculate the number of bars in each group
nbars = size(model_series, 2);

% Get the x coordinate of the bars
x = nan(nbars, ngroups);
for i = 1:nbars
    x(i, :) = b(i).XEndPoints;
end

disp('vaca');

% Plot the errorbars
errorbar(x', model_series, model_error, 'k','linestyle', 'none');

hold off