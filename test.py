# from my_tools import build_knowledge_base
#
# file_path = r'C:\Users\Administrator\langchain_chatbot\product.txt'
# knowledge_base = build_knowledge_base(file_path)
# answer = knowledge_base.invoke('请介绍一下上海的旅游产品')
# print(answer)


from agent import ConversationAgent

agent = ConversationAgent()
print(dir(ConversationAgent))
# agent.seed_agent()
# agent.generate_stage_analyzer(verbose=True)


# import re
#
# s = '("part1","part2")'
# pattern = r'\("([^"]*)","([^"]*)"\)'
#
# match = re.match(pattern, s)
#
# if match:
#     part1 = match.group(1)
#     part2 = match.group(2)
#     print("Part 1:", part1)
#     print("Part 2:", part2)
# else:
#     print("No match")




# file_path =r'C:\Users\Administrator\langchain_chatbot\product.txt'
# knowledge_base = build_knowledge_base(file_path)
# print(knowledge_base)
#
# answer = knowledge_base.invoke('上海三日游的产品价格是多少')
# print(answer)





# def check_content(pattern, text):
#     # 使用re.search检查字符串中是否存在匹配
#     if re.search(pattern, text):
#         return False
#     else:
#         return True
#
# pattern = r'\bquit\b'
#
# flag = True
# while flag:
#     agent.human_step()
#     agent.step()
#     history = agent.show_chat_history()
#     print(history)
#     agent.determine_conversation_stage()
#     flag = check_content(pattern,str(history[-2]))







