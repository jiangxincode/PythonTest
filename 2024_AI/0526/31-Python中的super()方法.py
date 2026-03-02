'''
问题：在Python代码中，如果子类重写了父类中的公共属性或公共方法，是父类中的属性或方法被删除了么？
答：不是的，子类对象 => 子类（有与父类相同的属性或方法） => 父类

问题：在重写的状态下，是否可以让子类调用父类中的方法呢？
答：可以，但是需要使用super()方法
'''
# 1. 定义一个父类（汽车类）
class Car(object):
    # 2. 定义公共属性
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    # 3. 定义公共方法
    def run(self):
        print('i can run!')

# 4. 定义一个汽油车
class GasolineCar(Car):
    # 5. 重写父类中的run()方法
    def run(self):
        print('i can run with gasoline!')

# 6. 定义一个电动车
class ElectricCar(Car):
    # 7. 重写__init__魔术方法
    def __init__(self, brand, model, battery):
        # 重用父类中__init__中的公共属性
        super().__init__(brand, model)
        # 子类拥有自己的属性
        self.battery = battery

    # 8. 重写run方法
    def run(self):
        print('i can run with electric!')

# 9. 实例化对象
tesla = ElectricCar('Tesla', 'Model Y', '72')
print(tesla.brand)
print(tesla.model)
print(tesla.battery)

tesla.run()