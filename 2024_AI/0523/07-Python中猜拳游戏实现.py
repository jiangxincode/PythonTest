'''
游戏角色：两个角色
玩家player
电脑computer

1. 玩家手工出拳：石头、剪刀、布 => input()
2. 电脑随机出拳：从石头、剪刀、布随机选择一个 => ?
3. 进行输赢比较
① 玩家获胜 => （石头 and 剪刀）
② 平局
③ 电脑获胜
普及一个知识点：
    and逻辑与，两边都是条件，如果两边条件同时成立，最终结果True，反之就是False
    or逻辑或，两边都是条件，如果只要有一边，条件为真，则最终结果True，反之就是False
相亲：
    女方A，自身条件较好，要求男方必须要有车 且 有房，才能牵手成功 => 有车 and 有房
    女方B，自身条件一般，要求男方有车 或者 有房，才能牵手成功 => 有车 or 有房

    = ：赋值
    == ：等于判断，判断两边的值是否相等
'''
from random import randint
# 1. 玩家手工出拳
player = int(input('请输入您的出拳信息(石头-1、剪刀-2、布-3）：'))
# 2. 电脑随机出拳
computer = randint(1, 3)
# 3. 输赢比较
if (player == 1 and computer == 2) or (player == 2 and computer == 3) or (player == 3 and computer == 1):
    print('玩家获胜')
elif player == computer:
    print('平局')
else:
    print('电脑获胜')