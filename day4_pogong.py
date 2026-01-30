import numpy as np
import matplotlib.pyplot as plt

x_data = np.array([1, 2, 3, 4])
y_data = np.array([450, 470, 485, 500])

print(f"数据已载入， X的形状：{x_data.shape}")
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, color='blue', label='Actual Scores')

plt.title("Exam Score Trend")
plt.xlabel("Exam Number")
plt.ylabel("Score")
plt.grid(True)

slope, intercept = np.polyfit(x_data, y_data, 1)
print(f"算出模型公式：y = {slope:.2f} * x + {intercept:.2f}")
y_predict = slope * x_data + intercept
plt.plot(x_data, y_predict, color='red', linewidth=2, label='Trend Line')
x_future = 5
score_future = slope * x_future + intercept
print(f"预测：第 {x_future} 次考试的分数大约是：{score_future:.2f}")
plt.scatter([x_future], [score_future], color='green', marker='*', s=200, label='Prediction')

plt.legend()
plt.show()