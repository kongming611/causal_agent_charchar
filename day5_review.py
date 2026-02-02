import numpy as np
import matplotlib.pyplot as plt
import mplcursors

x_data = np.array([1, 2, 3, 4])
y_data = np.array([450, 470, 485, 500])

k, b = np.polyfit(x_data, y_data, 1)
print(f"模型公式：y = {k:.2f}x + {b:.2f}")

x_future = 5
y_future = k * x_future + b
print(f"预测第五次分数：{y_future:.2f}")

## for i in range(len(x_data)):
   ## current_x = x_data[i]
    ##current_y = y_data[i]
    ##plt.text(current_x, current_y + 5, f"{current_y:.1f}", ha='center', va='bottom', fontsize=12)
## plt.text(x_future, y_future + 5, f"{y_future:.1f}", ha='center', va='bottom', fontsize=12, color='green')

x_line = np.array([1, 5])
y_line = k * x_line + b
plt.scatter(x_data, y_data, color='blue', label='History')
plt.plot(x_line, k * x_line + b, color='red', linestyle='--', label='Trend')
plt.scatter([x_future], [y_future], color='green', marker='*', s=200, label='Prediction')
mplcursors.cursor(hover=True)
plt.legend()
plt.grid(True)
plt.show()