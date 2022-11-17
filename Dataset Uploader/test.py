test = ['test', '10']
new_list = [int(element) for element in test if element.isdigit()]

print(new_list)
for ele in new_list:
    print(type(ele))