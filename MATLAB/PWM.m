function [f_PWM] = PWM(freq, offsetIndex, amp, duty, t)
% Create PWM signal

% freq [Hz]
% offsetindex [# of indeces]
% amp []
% duty [%]
% t [vector]

f_PWM = amp*square(2*pi*freq.*t,duty);
original_length = length(f_PWM);
f_PWM = [zeros(1, offsetIndex), f_PWM];
f_PWM = f_PWM(1:(original_length));


% Logical indexing to find the -1 values
idx = f_PWM == -amp;

% Replace the -1 values with zeros
f_PWM(idx) = 0;

end