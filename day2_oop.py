class StudentAgent:
    def __init__(self, name, major):
        self.name = name
        self.major = major
        self.scores = []
        self.history = []
        print(f"智能体 {self.name} 初始化完成！")

    def add_score(self, score):
        self.scores.append(score)
        print(f"{self.name} 录入成绩 {score}")

    def speak(self, content):
        self.history.append(content)
        print(f"{self.major} {self.name} 说: {content}")

    def recall(self):
        print(f"\n --- 开始读取 {self.name} 的记忆 ---")
        for i, msg in enumerate(self.history):
            print(f"记忆片段 {i + 1}: {msg}")

agent = StudentAgent("钟江铭", "材料类")
agent2 = StudentAgent("蕾蕾", "应用心理学")

agent.speak("你好，我是材料类学生创作的Agent！")
agent.speak("我刚刚弄懂了Python的类和对象。")

agent.add_score(85)
agent.add_score(95)

agent2.add_score(100)
agent2.speak("我是蕾蕾，我考了满分！")

agent.recall()

# print(f"最后一次成绩是 {agent.scores[-1]}")
print(f"{agent.major} {agent.name} 的分数列表: {agent.scores}")
print(f"蕾蕾的分数列表: {agent2.scores}")