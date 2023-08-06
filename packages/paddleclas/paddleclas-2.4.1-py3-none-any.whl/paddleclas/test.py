#packages = [2,7,9,3,5]
#packages = [2,7,9,3,5]
packages = [2,29,1,26,5,8,3,9]

max_list = [packages[-1]]
max_list_p = 0
for i in range(len(packages)-2, -1, -1):
    if packages[i] < max_list[max_list_p]:
        max_list[max_list_p] += packages[i]
    else:
        max_list.append(packages[i])
        max_list_p += 1

print(max(max_list))
