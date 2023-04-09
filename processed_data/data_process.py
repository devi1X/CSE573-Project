import pandas as pd


def file_spliter(parent_file, child_file_prefix, start, end, max_size):
    # read csv file into dataframe form
    data = pd.read_csv(parent_file)

    index = 0
    while start < len(data):
        # set start and end pivot for partitioning
        file_end_index = start + max_size

        if end > len(data):
            child_data = data[start: len(data)]
        else:
            child_data = data[start: end]

        child_data.to_csv(f"{child_file_prefix}{index + 1}.csv", index=False)
        index += 1
        start = end


def file_merger(file_list):
    df_list = []

    for file in file_list:
        df = pd.read_csv(file)
        df_list.append(df)

    sum_file = pd.concat(df_list)
    sum_file.to_csv('result.csv', index=False)


def main():
    parent_file = "merged_file.csv"
    child_file_prefix = "split_file"
    file_list = ['result1.csv', 'result2.csv', 'result3.csv', 'result4.csv', 'result5.csv']
    file_start_index = 0
    file_end_index = 0
    max_file_size = 200

    # todo: choose one method to implement
    # file_spliter(parent_file, child_file_prefix, file_start_index, file_end_index, max_file_size)
    # file_merger(file_list)


if __name__ == '__main__':
    main()

