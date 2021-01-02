
replace_lines = []
with open('beibei.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        tags = line.split('\t')
        if len(tags) !=5:
            print(tags)
        replace_lines.append((',').join(tags))

with open('newbeibei.csv','w') as nf:
    nf.writelines(replace_lines)