'''
什么是重写？不仅要继承父类中的公共属性和公共方法，子类也要有属于自己的属性和方法，否则继承就失去意义。
答：所谓的重写，就是子类拥有与父类相同的属性或方法，子类对象相同属性或方法时，子类中的属性和方法，会自动覆盖父类中的属性和方法
父类有一个speak()方法
子类有一个speak()方法
则子类的会覆盖父类中的speak方法 => 重写机制
'''
class Animal(object):
    # 1. 定义公共属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 2.定义公共方法
    def sound(self):
        print('i can sound!')

class Dog(Animal):
    # 3. 定义一个重写方法
    def sound(self):
        print('i can wang wang wang!')

class Cat(Animal):
    # 4. 定义一个重写方法
    def sound(self):
        print('i can miao miao miao!')

# 5. 实例化对象
dog = Dog('史努比', 6)
dog.sound()

cat = Cat('加菲猫', 5)
cat.sound()