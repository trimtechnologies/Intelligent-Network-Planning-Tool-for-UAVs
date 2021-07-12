y1 = [
    2.194  2.145  2.126  2.115 2.115 2.115
    2.01  2.098  2.136  2.136 2.136 2.115
    2.1  2.105  2.111  2.115 2.115 2.115
    2.155  2.133  2.187  2.192 2.192 2.115
    2.155  2.133  2.187  2.192 2.291 2.115
    2.155  2.133  2.187  2.192 2.291 2.115
];

err1=[
    0.002  0.004  0.011  0.005 0.005 0.005 
    0.019  0.006  0.003  0.008 0.008 0.005 
    0.008  0.007  0.011  0.007 0.007 0.005 
    0.013  0.016  0.013  0.019 0.019 0.005 
    0.013  0.016  0.013  0.019 0.019 0.005 
    0.013  0.016  0.013  0.019 0.019 0.005 
  ];

hBar = bar(y1,1);                                                   % Return ‘bar’ Handle
for k1 = 1:size(y1,1)
    ctr(k1,:) = bsxfun(@plus, hBar(1).XData, hBar(k1).XOffset');    % Note: ‘XOffset’ Is An Undocumented Feature; This Selects The ‘bar’ Centres
    ydt(k1,:) = hBar(k1).YData;                                     % Individual Bar Heights
end
hold on

disp(ctr);


errorbar(ctr, ydt, err1, '.r');                                      % Plot Erro

hold off
ylim ([1.8 2.4])
title('Hardened density')
grid on 
grid minor
legend ('CON','MK20','nS1', 'gMean','location','NW')
xlabel('Mortar Type') % x-axis label
ylabel('Density (g/m^3)') % y-axis label
set(gca,'XTickLabel',{'Accuracy','Sensitivity','Precision', 'F-Measure', 'G-mean', 'AUC'})