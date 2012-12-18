%% Machine Learning Online Class - Exercise 2: Logistic Regression
%
%  Instructions
%  ------------
% 
%  This file contains code that helps you get started on the second part
%  of the exercise which covers regularization with logistic regression.
%
%  You will need to complete the following functions in this exericse:
%
%     sigmoid.m
%     costFunction.m
%     predict.m
%     costFunctionReg.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% Initialization
clear ; close all; clc

%% Load Data
%  The first two columns contains the X values and the third column
%  contains the label (y).

data_train = load('train_output.csv');
data_test = load('test_output.csv');

X = data_train(:, 2); y = data_train(:, 1);
X_test = data_test(:, 1);
%X = data_train(:, [2, 3, 4, 5, 6, 7]); y = data_train(:, 1);
%X_test = data_test(:, [1, 2, 3, 4, 5, 6]);

y_test = zeros(size(X_test(:,1))); 

%Add ones to X
X = [ones(size(X(:,1))) X];
X_test = [ones(size(X_test(:,1))) X_test];

%add polynomial degree
%X_mapped = mapFeature(X(:,4), X(:,2));
%X = [X_mapped X(:,3) X(:,5) X(:,6) X(:,7)];
%X_test_mapped = mapFeature(X_test(:,4), X_test(:,2));
%X_test = [X_test_mapped X_test(:,3) X_test(:,5) X_test(:,6) X_test(:,7)];


% Initialize fitting parameters
initial_theta = zeros(size(X, 2), 1);

% Set regularization parameter
lambda = 0.4;

%for lambda=0:0.1:1
% Compute and display initial cost and gradient for regularized logistic
% regression
[cost, grad] = costFunctionReg(initial_theta, X, y, lambda);


% Initialize fitting parameters
initial_theta = zeros(size(X, 2), 1);

% Set Options
options = optimset('GradObj', 'on', 'MaxIter', 400);

% Optimize
[theta, J, exit_flag] = ...
	fminunc(@(t)(costFunctionReg(t, X, y, lambda)), initial_theta, options);


% Compute accuracy on our training set

treshold = 0.5;
%for t=0:0.01:1
p = predict(theta, X, treshold);
fprintf('Treshold: %f\n', treshold);
%fprintf('Lambda: %f\n', lambda);
fprintf('Train Accuracy: %f\n', mean(double(p == y)) * 100);
%end

theta

%Predict test results
y_test = predict(theta,X_test,treshold);
save result.txt y_test;

