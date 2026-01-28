
import numpy as np

vec_3d = np.array([10, 20, 30])
print(f"向量A的维度：{vec_3d.shape}")

vec_4d = np.array([180, 70, 25, 95])
print(f"向量B的维度：{vec_4d.shape}")

student1 = np.array([180, 70, 25, 95])
student2 = np.array([175, 65, 26, 90])

diff = student1 - student2

print(f"两个人的差距向量：{diff}")

'''

list1 = [180, 70, 25, 95]
list2 = [175, 65, 26, 90]

result = []
for i in range(len(list1)):
    val = list1[i] - list2[i]
    result.append(val)

print(f"成绩差距是：{result}")

'''