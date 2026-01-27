class Dog:
    def __init__(self, name):
        self.name = name
        self.scores = []

    def bark(self):
        print(f"{self.name}在汪汪叫")

    def add_score(self , score):
        self.scores.append(score)
        print(f"{self.name}记下了一个分数：{score}")

    def show_scores(self):
        print(f"---{self.name}的成绩单---")
        for s in self.scores:
            print(f"分数：{s}")

dog1 = Dog("来福")
# dog2 = Dog("旺财")

dog1.add_score(100)
dog1.add_score(200)

dog1.show_scores()

#dog1.bark()
# dog2.bark()