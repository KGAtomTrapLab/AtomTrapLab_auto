v  = table2array(testScan(:,5));
y1 = table2array(testScan(:,1));
y2 = table2array(testScan(:,2));
y3 = table2array(testScan(:,3));
y4 = table2array(testScan(:,4));
% y5 = table2array(testScan(:,5));
% y6 = table2array(testScan(:,6));
% y7 = table2array(testScan(:,7));

% y_test = table2array(comp_test(:,3));
% y_wrong = table2array(comp_test(:,1));
% y_wrong2 = table2array(comp_test(:,2));
% y_wrong3 = table2array(comp_test(:,4));

% r = mean(xcorr(y3,'normalized'))
% rxy = mean(xcorr(y3,y_test,'normalized'))
% r_test = mean(xcorr(y3,y_wrong,'normalized'))
% r_test2 = mean(xcorr(y3,y_wrong2,'normalized'))
% r_test3 = mean(xcorr(y3,y_wrong3,'normalized'))
for i = 1:length(y1)
    a = y1(i);
    if a < 0.1
        y1(i) = 0;
    end
end

y1 = lowpass(y1,0.11);
y3 = lowpass(y3,0.01);
figure(3)
plot(v,y1)

figure(1)
subplot(2,2,1)



plot(v,y1)

subplot(2,2,2)
plot(v,y2)

subplot(2,2,3)
plot(v,y3)

subplot(2,2,4)
plot(v,y4)

%% Use findpeaks
figure(5)
[pks,locs] = findpeaks(y1(50:end),'npeaks',100);

findpeaks(y1(50:end),'npeaks',4);
text(locs+.02,pks,num2str((1:numel(pks))'))
