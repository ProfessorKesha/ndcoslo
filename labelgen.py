import os
import random
from pathlib import Path
import time

def main(main_folder, train_valid_test_split, seed, version):
    
    # set random seed so that we can get deterministic runs
    random.seed(seed)
    
    # define paths
    main_folder_path = Path(main_folder)
    train_lst = main_folder_path/f'{main_folder}_train_v{version:03}.lst'
    valid_lst = main_folder_path/f'{main_folder}_valid_v{version:03}.lst'
    test_lst = main_folder_path/f'{main_folder}_test_v{version:03}.lst'
    train_pc, valid_pc, test_pc = train_valid_test_split
    assert train_pc + valid_pc + test_pc == 1, f'Split percentages do not sum up to 1: {train_valid_test_split}'
    
    # some counters
    global_id = 0
    class_id = 0
    train_count = 0
    valid_count = 0
    test_count = 0
    print()
    imgs = []
    
    # iterate through each subfolder
    for subfolder in os.scandir(main_folder):
        
        if subfolder.is_dir():
            
            print(f'Processing subfolder: {subfolder.path}')
            
            # get list of all images in this subfolder
            imgs += [[class_id, f] for f in Path(subfolder.path).glob('*.jpg')]
            
            # global_id += 1
            class_id += 1
            
    with open(train_lst, 'w') as f_train, open(valid_lst, 'w') as f_valid, open(test_lst, 'w') as f_test:
        
        # shuffle the image order
        random.shuffle(imgs)
        
        # write out file
        for img in imgs:
            
            r = random.random()
            line = f'{global_id}\t{img[0]}\t{img[1].relative_to(main_folder).as_posix()}\n'
            
            if r <= train_pc:
                f_train.write(line)
                train_count += 1
            elif r > train_pc and r <= train_pc+valid_pc:
                f_valid.write(line)
                valid_count += 1
            else:
                f_test.write(line)
                test_count += 1
                
            global_id += 1
            
    print()
    print(f'{train_count} train, {valid_count} valid, {test_count} test')
    print(f'lst files generated: {train_lst}, {valid_lst}, {test_lst}')
    
    
if __name__ == '__main__':
    
    # user inputs
    main_folder = 'flowers'
    train_valid_test_split = [0.882, 0.098, 0.02]
    version = 2
    seed = 0
    
    # print user inputs
    print()
    print(f'main folder: {main_folder}')
    print(f'train/valid/test split: {train_valid_test_split}')
    print(f'seed: {seed}')
    
    # call the main function
    start = time.time()
    main(main_folder, train_valid_test_split, seed, version)
    end = time.time()
    print()
    print(f'time taken: {end-start:.4f} seconds')