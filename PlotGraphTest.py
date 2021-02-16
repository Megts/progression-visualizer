

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

#plt.style.available (This will show the different styles we can use)
plt.style.use('ggplot')

#X and Y axis data input
date_x = [1,2,3]
A1performance = [6.89, 6.70, 6.43]
A2performance= [6.99, 6.81, 6.70]

#Calling the input data to be plotted
plt.plot(date_x, A1performance, color='k', linestyle='--', marker= 'o', label='Athlete1')
plt.plot(date_x, A2performance, color='k', linestyle='--', marker= '.', label= 'Athlete2')

#Graph labels
plt.title("Athlete Performances")
plt.xlabel("Date")
plt.ylabel("Performance Time/Distance")

plt.legend()
plt.grid(True)
plt.show()
