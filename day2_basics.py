# 数组
scores = [450, 470, 485]
scores.append(500)
print("分数列表：", scores)

# 负数索引
last_score = scores[-1]
print("最新一次分数", last_score)

# 切片
first_two = scores[:2]
print("前两次分数", first_two)

last_three = scores[-3:]
print("后三次分数", last_three)

middle_two = scores[1:3]
print("中间两次分数", middle_two)

# 遍历
for score in scores:
    print(f"成绩为：{score}")

# 枚举
for index, score in enumerate(scores):
    print(f"第{index + 1}次考试的成绩是{score}")

for i, score in enumerate(scores):
    if score > 480:
        print(f"第{i + 1}次考了{score}分，不错哟")
    else:
        print(f"第{i + 1}次考了{score}分，继续加油")


