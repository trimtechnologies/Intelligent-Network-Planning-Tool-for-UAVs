x=categorical({'Accuracy','Sensitivity','Precision', 'F-Measure', 'G-mean', 'AUC'});

z=[
    0.82, 0.84, 0.81, 0.80, 0.77, 0.79;
    0.86, 0.89, 0.85, 0.85, 0.82, 0.84;
    0.87, 0.90, 0.86, 0.86, 0.83, 0.85;
    0.90, 0.93, 0.89, 0.88, 0.85, 0.87;
    0.96, 0.96, 0.94, 0.94, 0.92, 0.93;
    0.94, 0.94, 0.94, 0.90, 0.91, 0.90;
    0.99, 0.99, 0.98, 0.97, 0.94, 0.96;
    ];

y=transpose(z);

a=[
    0.01, 0.08, 0.02, 0.03, 0.04, 0.02;
    0.02, 0.05, 0.02, 0.05, 0.03, 0.04;
    0.05, 0.03, 0.06, 0.04, 0.03, 0.04;
    0.01, 0.02, 0.03, 0.02, 0.02, 0.02;
    0.02, 0.01, 0.01, 0.01, 0.02, 0.01;
    0.01, 0.01, 0.01, 0.01, 0.02, 0.01;
    0.01, 0.01, 0.01, 0.01, 0.02, 0.01;
    ];

errorplus=a;
errorminus=errorplus;
figure;
bar(x,y);
hBar = bar(y, 0.8);

for k1 = 1:size(y,2)
    ctr(k1,:) = bsxfun(@plus, hBar(k1).XData, hBar(k1).XOffset');     
    ydt(k1,:) = hBar(k1).YData;                    
end

hold on
errorbar(ctr, ydt, errorplus, '.k')                  
hold off
legend ('NB', 'SVM', 'RF', 'MP', 'CNN BLSTM-RNN(ReLU)', 'CNN BLSTM-RNN(Softmax)', 'CNN BLSTM-RNN(SRS)', 'location','NW', 'Orientation', 'horizontal', 'FontSize', 22);
ylabel('Performance Measure', 'FontSize', 28);
set(gca,'linewidth', 2, 'FontSize', 28);
ylim([0 1.15]);
set(gca,'XTickLabel', x)
