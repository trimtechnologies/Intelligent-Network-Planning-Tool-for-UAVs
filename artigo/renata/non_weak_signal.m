x=categorical({'Accuracy','Sensitivity','Precision', 'F-Measure', 'G-mean', 'AUC'});

z=[
    0.80, 0.83, 0.78, 0.78, 0.76, 0.78;
    0.83, 0.86, 0.82, 0.81, 0.78, 0.80;
    0.84, 0.87, 0.83, 0.82, 0.79, 0.81;
    0.88, 0.91, 0.87, 0.86, 0.83, 0.85;
    0.93, 0.96, 0.92, 0.92, 0.89, 0.90;
    0.92, 0.94, 0.91, 0.90, 0.87, 0.88;
    0.96, 0.99, 0.96, 0.94, 0.91, 0.93;
    ];

y=transpose(z);

a=[
    0.05, 0.04, 0.10, 0.06, 0.06, 0.04;
    0.07, 0.03, 0.08, 0.06, 0.05, 0.03;
    0.02, 0.05, 0.07, 0.04, 0.02, 0.06;
    0.02, 0.01, 0.04, 0.03, 0.03, 0.03;
    0.02, 0.01, 0.03, 0.02, 0.01, 0.02;
    0.02, 0.01, 0.03, 0.02, 0.01, 0.02;
    0.02, 0.01, 0.03, 0.02, 0.01, 0.02;
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

