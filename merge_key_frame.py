import numpy as np

def sort_by_first_element(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    data = [line.strip().split() for line in lines]
    data = [(float(line[0]), line) for line in data]

    sorted_data = sorted(data, key=lambda x: x[0])
    sorted_filename = 'sorted_' + filename
    with open(sorted_filename, 'w') as sorted_file:
        for _, line in sorted_data:
            sorted_file.write(
                str(line[0])+' '+str(line[1])+' '+str(line[2])+' '+str(line[3])+' '+str(line[4])
                +' '+str(line[5])+' '+str(line[6])+' '+str(line[7])+'\n'
            )

    print("File sorted and saved as", sorted_filename)
    return sorted_filename


def remove_duplicates(input_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    seen_lines = set()
    unique_lines = []

    for line in lines:
        if line not in seen_lines:
            seen_lines.add(line)
            unique_lines.append(line)
    output_filename = 'unique_'+input_filename
    with open(output_filename, 'w') as unique_file:
        unique_file.writelines(unique_lines)

    print("Duplicates removed. Unique content saved in", output_filename)
    return output_filename
    


def alined_frame(key_frame_file,time_frame_file,save_file):
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
        print("Alined Success! Sorting")
        sort_file = sort_by_first_element(save_file)
        unique_filename = remove_duplicates(sort_file)
        
        final_file = 'result_frame.txt'
        init_time = 1691140902.914534-988.0165722-2.6
        with open(unique_filename,'r') as ufile:
            ulines = ufile.readlines()
        with open(final_file,'a') as ffile:
            ffile.truncate(0)
        for uline in ulines:
            uelements = uline.strip().split()
            origin_time = float(uelements[0])
            # y = 0.001106x^2-1.348x+1157.393
            # uelements[0] = np.power(float(uelements[0]),2)*0.001106- 1.348*float(uelements[0])+1157.393
            # uelements[0] = uelements[0]+1691140000.000
            uelements[0] = float(uelements[0]) + init_time
            with open(final_file,'a') as ffile:
                ffile.write(
                    str(uelements[0])+' '+str(uelements[1])+' '+str(uelements[2])+' '+str(uelements[3])+' '+str(uelements[4])
                    +' '+str(uelements[5])+' '+str(uelements[6])+' '+str(uelements[7])+' '+str(origin_time)+'\n'
                )
        

        

if __name__ == "__main__":    
    
    time_frame_file = 'time_frame.txt'
    key_frame_file = 'key_frame.txt'
    save_file = 'aft_frame.txt'
    alined_frame(key_frame_file,time_frame_file,save_file)

    