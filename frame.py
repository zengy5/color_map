import numpy as np


def sort_by_first_element(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 将每行拆分成列表，并转换第一个元素为浮点数
    data = [line.strip().split() for line in lines]
    data = [(float(line[0]), line) for line in data]

    # 按第一个元素排序
    sorted_data = sorted(data, key=lambda x: x[0])

    # 将排序后的数据写入新的txt文件
    sorted_filename = 'sorted_' + filename
    with open(sorted_filename, 'w') as sorted_file:
        for _, line in sorted_data:
            sorted_file.write(
                str(line[0])+' '+str(line[1])+' '+str(line[2])+' '+str(line[3])+' '+str(line[4])
                +' '+str(line[5])+' '+str(line[6])+' '+str(line[7])+'\n'
            )

    print("File sorted and saved as", sorted_filename)


def remove_duplicates(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # 使用集合来存储已经出现过的行
    seen_lines = set()

    # 存储非重复行的列表
    unique_lines = []

    for line in lines:
        if line not in seen_lines:
            seen_lines.add(line)
            unique_lines.append(line)

    # 将非重复行写入新文件
    with open(output_filename, 'w') as unique_file:
        unique_file.writelines(unique_lines)

    print("Duplicates removed. Unique content saved in", output_filename)




def alined_frame(key_frame_file,time_frame_file,save_file,init_time):
# process real time
    with open(time_frame_file, 'r' ) as tfile:
        tlines = tfile.readlines()

    time_origin = np.zeros(len(tlines)) 
    i = 0   
    for tline in tlines:
        time_origin[i] = float(tline)
        i += 1

    # process key frame
    with open(key_frame_file,'r') as kfile:
        klines = kfile.readlines()

    if len(time_origin) != len(klines):
        print("Error, length isn't equal")    
        
    else:
        if init_time:
            time_origin = time_origin + init_time
        k = 0
        with open(save_file,'a') as sfile:
            sfile.truncate(0)
            
        for kline in klines:
            elements = kline.strip().split()
            with open(save_file,'a') as sfile:
                sfile.write(
                    str(time_origin[k])+' '+str(elements[1])+' '+str(elements[2])+' '+str(elements[3])+' '+str(elements[4])
                    +' '+str(elements[5])+' '+str(elements[6])+' '+str(elements[7])+'\n'
                )
            k += 1
        print("Alined Success! Saved in ",save_file)
    
if __name__ == "__main__":    
    
    time_frame_file = 'time_frame.txt'
    key_frame_file = 'key_frame.txt'
    save_file = 'aft_frame.txt'
    init_time = 1687246711.0561743+0.7-9465.0134075
    # init_time  = 0
    alined_frame(key_frame_file,time_frame_file,save_file,init_time)
    
    # input_filename = 'aft_frame.txt'
    # sort_by_first_element(input_filename)

    input_filename = 'sorted_aft_frame.txt'
    output_filename = 'unique_data.txt'
    remove_duplicates(input_filename, output_filename)
    